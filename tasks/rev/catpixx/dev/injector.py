import re
from glob import glob

from string import ascii_lowercase

FLAG = "ctfcup{suchnicec4tpixxwo4h}"
SECRET = b"5uper_Dup3r Secret String!1"

assert len(FLAG) == len(SECRET)

LOSE_METHOD = """
.method public static {name}()V
    .registers 3

    invoke-static {{ }}, Landroid/app/ActivityThread;->currentApplication()Landroid/app/Application;

    move-result-object v0

    invoke-virtual {{v0}}, Landroid/app/Application;->getApplicationContext()Landroid/content/Context;

    move-result-object v0

    const-string v1, "Wrong! gas leak"

    const v2, 0x1

    invoke-static {{v0, v1, v2}}, Landroid/widget/Toast;->makeText(Landroid/content/Context;Ljava/lang/CharSequence;I)Landroid/widget/Toast;

    move-result-object v0

    invoke-virtual {{v0}}, Landroid/widget/Toast;->show()V

    return-void
.end method
"""

# params: letter, index, xor, xor_res, fail_handler, next_letter_class, next_letter_method
LETTER_CHECKER_METHOD = """
.method public static {letter}(Ljava/lang/String;)V
    .registers 3
    # v0, v1, v2=p0

    const v0, {index}

    invoke-virtual {{p0, v0}}, Ljava/lang/String;->codePointAt(I)I

    move-result v1

    const v0, {xor}

    xor-int v0, v0, v1

    const v1, {xor_res}

    if-eq v0, v1, :ok

    invoke-static {{ }}, L{fail_handler};->{fail_handler_method}()V

    return-void

    :ok

    invoke-static {{p0}}, L{next_letter_class};->{next_letter_method}(Ljava/lang/String;)V

    return-void
.end method

"""

# params: letter, length, fail_handler, next_letter_class, next_letter_method
LENGTH_CHECKER_METHOD = """
.method public static {name}(Ljava/lang/String;)V
    .registers 3
    # v0, v1, v2=p0

    invoke-virtual {{p0}}, Ljava/lang/String;->length()I

    move-result v0

    const v1, {length}

    if-eq v0, v1, :ok

    invoke-static {{ }}, L{fail_handler};->{fail_handler_method}()V

    return-void

    :ok

    invoke-static {{ p0 }}, L{next_letter_class};->{next_letter_method}(Ljava/lang/String;)V

    return-void
.end method
"""

WIN_METHOD = """
.method public static {name}(Ljava/lang/String;)V
    .registers 2

    new-instance v0, Ljava/lang/UnsupportedOperationException;

    const-string v1, "Easter egg not implemented yet, sorry"

    invoke-direct {{v0, v1}}, Ljava/lang/UnsupportedOperationException;-><init>(Ljava/lang/String;)V

    throw v0

    return-void
.end method
"""

def smali_candidates(apk_dir: str) -> dict[str, str]:
    result = {}

    for fn in glob(f"{apk_dir}/smali/**/*.smali", recursive=True):
        with open(fn) as f:
            source = f.read()

        decls = re.findall(r"^\.(?:field|method)\s(?:\w+\s)*([a-z])[(:]", source, flags=re.MULTILINE)  # ) <- vim fix 
        if not decls:
            continue

        last_decl: str = max(decls)

        if last_decl.startswith("z"):
            # skip this class to avoid conflict
            continue

        result[fn] = chr(ord(last_decl) + 1)

    return result


def invert_dict(d: dict) -> dict:
    result = dict.fromkeys(set(d.values()), None)
    for k, v in d.items():
        if result[v] is None:
            result[v] = [] 
        result[v].append(k)
    return result


def get_class_name(filename: str) -> str:
    return "/".join(filename[filename.index("smali"):].split("/")[1:]).removesuffix(".smali")


def inject_method(filename: str, source: str):
    print(f"Injecting into {filename}")
    with open(filename, "a") as f:
        print(file=f)
        print(source, file=f)

if __name__ == "__main__":
    import sys
    import random

    random.seed(0x1338BEED)

    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <apktool output dir>", file=sys.stderr)
        exit(2)

    patches = {}

    candidates = smali_candidates(sys.argv[1])
    short_classes = [path for path in candidates if get_class_name(path).count("/") == 1]
    long_classes = [path for path in candidates if get_class_name(path).count("/") > 1]
    all_classes = list(candidates.keys())
    letter_to_classes = invert_dict(candidates)
    
    # 1. Inject fail method
    fail_class = random.choice(long_classes)
    fail_method = candidates[fail_class]
    patches[fail_class] = LOSE_METHOD.format(name=fail_method)

    # 2. Inject win method
    last_class = random.choice(long_classes)
    if last_class in patches:
        raise ValueError(f"try another seed")
    last_method = candidates[last_class]
    patches[last_class] = WIN_METHOD.format(name=last_method)

    # 3. Inject letter checkers

    # Shuffle secret
    secret_indices = list(enumerate(SECRET))
    random.shuffle(secret_indices)

    for flag_letter, (index, secret_letter) in zip(FLAG[::-1], secret_indices):
        xor_value = random.randrange(256) 
        xor_letter = secret_letter ^ xor_value

        method_name = flag_letter if flag_letter in ascii_lowercase else hex(ord(flag_letter))[1:]
 
        # params: letter, index, fail_handler, next_letter_class, next_letter_method
        source = LETTER_CHECKER_METHOD.format(
            letter = method_name,
            index = hex(index),
            xor = hex(xor_value),
            xor_res = hex(xor_letter),
            fail_handler = get_class_name(fail_class),
            fail_handler_method = fail_method,
            next_letter_class = get_class_name(last_class),
            next_letter_method = last_method
        )

        if method_name != flag_letter:
            # letter was hex encoded, use any class
            last_class = random.choice(short_classes)
        else:
            last_class = random.choice(list(set(letter_to_classes[flag_letter]) - set(long_classes)))
            if last_class in patches:
                raise ValueError(f"try another seed")

        patches[last_class] = source
        last_method = method_name

    # 4. Inject length checker

    length_checker_class = random.choice(long_classes)
    if length_checker_class in patches:
        raise ValueError(f"try another seed")

    source = LENGTH_CHECKER_METHOD.format(
        name = candidates[length_checker_class],
        length = hex(len(SECRET)),
        fail_handler = get_class_name(fail_class),
        fail_handler_method = fail_method,
        next_letter_class = get_class_name(last_class),
        next_letter_method = last_method
    )

    patches[length_checker_class] = source

    for it in patches.items():
        inject_method(*it)

