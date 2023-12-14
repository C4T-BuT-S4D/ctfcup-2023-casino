const puppeteer = require('puppeteer')
const sleep = async ms => new Promise(resolve => setTimeout(resolve, ms))

let browser = null

const visit = async url => {
	let context = null
	try {
		if (!browser) {
			const args = ['--js-flags=--jitless,--no-expose-wasm', '--disable-gpu', '--disable-dev-shm-usage', '--no-sandbox']
			if (new URL(url).protocol === 'http:') {
				args.push(`--unsafely-treat-insecure-origin-as-secure=${url}`)
			}
			browser = await puppeteer.launch({
				headless: 'new',
				args
			})
		}
		if( !(['http:', 'https:'].includes(new URL(url).protocol)))
            return "Provice a valid url";
		context = await browser.createIncognitoBrowserContext()
		const page1 = await context.newPage()
		await page1.goto(process.env.TASK_URL);
		const flag = proccess.env.FLAG;
		page1.evaluate(() => {
			localStorage.setItem('savedCodes',flag);
		},{flag});
		await sleep(2000)
		await page1.goto(url)
		await sleep(2000)
		await page1.close()
		await context.close()
		context = null
	} catch (e) {
		console.log(e)
	} finally {
		if (context) await context.close()
	}
}
module.exports = visit;