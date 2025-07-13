import { extract_text } from "../../node/extract_text/build/lib.js"
import fs from "node:fs";

main();
function get_title(data: string) {
	let start = data.search("<title>");
	let end = data.search("</title>");
	if (start === -1 || end === -1) return "no title";
	let title = data.slice(start + 7, end);
	title = title.replace(/\n/, "").trim();
	return title;
}
async function main() {
	let filename = process.argv[2];
	if(!filename) throw new Error("need filename");
	if (filename.startsWith("./"))
		filename = filename.slice(2);
	let file_content = fs.readFileSync(filename).toString();
	let file_content_splt = file_content.split("\n");
	let url_str = file_content_splt[2];
	url_str = url_str.slice(6);
	let title = get_title(file_content);
	let url = URL.parse(url_str);
	let text = await extract_text(filename, url);
	let index_url = "http://localhost:33101/addpage"
	let archive_url = `https://oldsite.github.io/${filename}`
	let msg = {
		title: title,
		body: text,
		url: encodeURI(archive_url),
	};
	let msg_json = JSON.stringify(msg);
	fetch(index_url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: msg_json
	})
	.then(response => {
		if (!response.ok) {
			console.log(response);
			throw new Error(`Network response was not ok`);
		}
		return response.json();
	})
	.then(data => {
		// console.log('Success:', data);
	})
	.catch(error => {
		console.error('Error:', error);
	});

}
