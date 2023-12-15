const express = require('express');
const axios = require('axios');
const session = require('express-session');
const bodyParser = require('body-parser');
const app = express();
const port = 3000;

app.use(session({
  secret: 'secret-key',
  resave: false,
  saveUninitialized: true
}));

async function getCTFTeams() {
  return [{"name":"More Smoked Leet Chicken","id":1005,"ratingPoints":670.814407817,"score":0},{"name":"IV","id":1006,"score":0},{"name":"gd","id":1007,"ratingPoints":0.664374734998,"score":0},{"name":"GG","id":1008,"ratingPoints":10.3024067171,"score":0},{"name":"c4","id":1009,"ratingPoints":1.96885103701,"score":0},{"name":"ti","id":1010,"score":0},{"name":"qq","id":1011,"ratingPoints":5.97865092516,"score":0},{"name":"cw","id":1012,"score":0},{"name":"IU","id":1013,"ratingPoints":0.124084249084,"score":0},{"name":"OL","id":1014,"score":0},{"name":"XK","id":1015,"score":0},{"name":"..","id":1016,"ratingPoints":0.960235547114,"score":0},{"name":"ev","id":1017,"score":0},{"name":"EpicFail","id":1019,"score":0},{"name":"ACME Pharmaceuticals","id":1020,"ratingPoints":6.08159963014,"score":0},{"name":"+++","id":1021,"score":0},{"name":"nibbles","id":1022,"score":0},{"name":"As it were Antani","id":1023,"score":0},{"name":"0xABC","id":1024,"ratingPoints":0.37057893831,"score":0},{"name":"choding","id":1025,"score":0},{"name":"0xBeer","id":1027,"score":0},{"name":"octahedron","id":1028,"score":0},{"name":"We Test Pens","id":1029,"score":0},{"name":"pijemy w chuj","id":1030,"score":0},{"name":"gungho","id":1031,"score":0},{"name":"SecNoob","id":1032,"score":0},{"name":"GPF","id":1033,"score":0},{"name":"Synapse & Darpa","id":1034,"score":0},{"name":"N0rthK0r34","id":1035,"score":0},{"name":"SeHwa in CERT-IS","id":1036,"score":0},{"name":"C.R.Y","id":1037,"score":0},{"name":"ic3burn","id":1038,"score":0},{"name":"Left_RED","id":1039,"score":0},{"name":"KUICS","id":1040,"ratingPoints":5.63614872126,"score":0},{"name":"murlandia","id":1042,"score":0},{"name":"Neohapsis","id":1043,"score":0},{"name":"0day","id":1044,"ratingPoints":10.3672373358,"score":0},{"name":"justmyself","id":1045,"score":0},{"name":"Actimel","id":1046,"score":0},{"name":"IQBalance","id":1047,"score":0},{"name":"WetPuppies","id":1048,"score":0},{"name":"Dolomite","id":1049,"score":0},{"name":"THD","id":1051,"score":0},{"name":"helloWorld","id":1052,"ratingPoints":21.6638492693,"score":0},{"name":"매번나오는이상한팀","id":1054,"score":0},{"name":"nemesis","id":1055,"ratingPoints":1.2313935128,"score":0},{"name":"靑春","id":1056,"score":0},{"name":"viktorkbtu","id":1057,"score":0},{"name":"Assa","id":1058,"ratingPoints":12.4778727149,"score":0},{"name":"casper","id":1059,"ratingPoints":3.48398246551,"score":0},{"name":"il0cal","id":1060,"score":0},{"name":"ra","id":1061,"ratingPoints":2.47397983382,"score":0},{"name":"HQS","id":1062,"score":0},{"name":"alone4242","id":1063,"score":0},{"name":"LesPapasPingouins","id":1064,"score":0},{"name":"!(C)","id":1065,"score":0},{"name":"qallups","id":1066,"score":0},{"name":"masa","id":1067,"score":0},{"name":"Omni","id":1068,"score":0},{"name":"C.CR0W","id":1069,"score":0},{"name":"unkos","id":1070,"score":0},{"name":"noname","id":1071,"ratingPoints":75.4001717654,"score":0},{"name":"loossy","id":1072,"score":0},{"name":"hust","id":1073,"score":0},{"name":"trololo","id":1074,"score":0},{"name":"@egis","id":1075,"score":0},{"name":"Charrua","id":1076,"score":0},{"name":"Neko","id":1077,"ratingPoints":39.3474296852,"score":0},{"name":"HackTheLocal","id":1078,"score":0},{"name":"isg2011","id":1079,"score":0},{"name":"Rav3n","id":1080,"score":0},{"name":"chap","id":1081,"score":0},{"name":"diin","id":1082,"score":0},{"name":"zaregoto","id":1083,"score":0},{"name":"MA_CHAN","id":1084,"score":0},{"name":"isg","id":1085,"score":0},{"name":"math","id":1086,"score":0},{"name":"nesuw","id":1087,"score":0},{"name":"ARGOS with SUZY","id":1088,"score":0},{"name":"Кира","id":1089,"score":0},{"name":"uhdols","id":1090,"score":0},{"name":"shall","id":1091,"score":0},{"name":"gkistg","id":1092,"score":0},{"name":"JuanEscobar","id":1093,"score":0},{"name":"administwitter","id":1094,"score":0},{"name":"Tester","id":1095,"ratingPoints":6.94195266374,"score":0},{"name":"igrus_old","id":1096,"score":0},{"name":"d7795","id":1097,"score":0},{"name":"3rr0r","id":1098,"score":0},{"name":"disegin","id":1099,"score":0},{"name":"megapork","id":1100,"score":0},{"name":"bigbear","id":1101,"score":0},{"name":"hackerlogin","id":1102,"ratingPoints":0.551627523398,"score":0},{"name":"cat","id":1103,"ratingPoints":4.79325083064,"score":0},{"name":"O1db0Y","id":1104,"score":0},{"name":"l0ph3r","id":1106,"score":0},{"name":"Airwalk","id":1107,"score":0}]
}

function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

function initializeSession(req) {
  if (!req.session.teams || !req.session.currentTeamIndex) {
    req.session.teams = [];
    req.session.currentTeamIndex = 0;
    req.session.score = 0;
  }
}

async function generateNewTeams(req) {
  initializeSession(req);
  req.session.teams = await getCTFTeams();
  shuffleArray(req.session.teams);
}

app.get('/', async (req, res) => {
  await generateNewTeams(req);
  const selectedTeams = req.session.teams.slice(0, 2); // Выбираем две случайные команды
  res.send(`
    <h1>CTF Teams</h1>
    <form action="/vote" method="post">
      <label for="team">Выберите успешную команду:</label>
      <select name="team" id="team">
        ${selectedTeams.map((team, index) => `<option value="${index}">${team.name}</option>`).join('')}
      </select>
      <button type="submit">Отправить</button>
    </form>
  `);
});

app.post('/vote', bodyParser.urlencoded({ extended: true }), async (req, res) => {
  const selectedTeamIndex = parseInt(req.body.team, 10);

  const selectedTeamObject = req.session.teams[selectedTeamIndex];
  const opponentTeamIndex = (selectedTeamIndex + 1) % req.session.teams.length;
  const opponentTeamObject = req.session.teams[opponentTeamIndex];

  if (selectedTeamObject && opponentTeamObject) {
    console.log(selectedTeamObject.ratingPoints,opponentTeamObject.ratingPoints)
    if (selectedTeamObject.ratingPoints == opponentTeamObject.ratingPoints || selectedTeamObject.ratingPoints >= opponentTeamObject.ratingPoints) {
      req.session.score += 10000;
      res.send(`
        <h1>Правильный ответ!</h1>
        <p>Вы выбрали команду ${selectedTeamObject.name}. ${selectedTeamObject.name} успешнее!</p>
        <p>Ваши очки: ${req.session.score}</p>
        <a href="/">Продолжить игру</a>
        <a href="/flag">Получить флаг</a>
      `);
    } else {
      res.send(`
        <h1>Неправильный ответ!</h1>
        <p>Кажется, вы сделали ошибку в выборе команды. Попробуйте еще раз.</p>
      `);
    }
  } else {
    res.send(`
      <h1>Ошибка!</h1>
      <p>Что-то пошло не так. Пожалуйста, попробуйте еще раз.</p>
    `);
  }

  req.session.currentTeamIndex++;
  if (req.session.currentTeamIndex >= req.session.teams.length) {
    req.session.currentTeamIndex = 0;
  }
});
app.get('/flag',(req,res) => {
    if(req.session && req.session.score > 10000000)
        res.send(process.env.flag || 'test')
    else
        res.send("Похоже у тебя нет 10 миллионов");
})
app.listen(port, () => {
  console.log(`Server is running at http://localhost:${port}`);
});
