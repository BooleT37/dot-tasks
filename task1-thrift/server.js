#!/usr/bin/node

const http = require("http");
const thrift = require("thrift");
const MetaScrapper = require("./gen-nodejs/MetaScrapper");
const {InvalidUrl, NoMetadata, InvalidMetadata, Meta} = require("./gen-nodejs/task1_types");
const fetchUrl = require("fetch").fetchUrl;
const cheerio = require('cheerio');

const port = 9090;

var data = {};

function getMetaProp($, propName) {
	const node = $('meta[property=og\\:' + propName + ']');
	if (!node.length) {
		return null;
	}
	return node.attr('content');
}

function getMetaPropOrThrowError($, propName) {
	const value = getMetaProp($, propName);
	if (value === null) {
		throw new InvalidMetadata({message: `No ${propName} prop`});
	}
	if (!value.length) {
		throw new InvalidMetadata({message: `Title prop cannot ${propName} be empty`});
	}
	return value;
}

function setMetaPropIfExists(meta, $, propName, propAttribute) {
	if (!propAttribute) {
		propAttribute = propName;
	}
	const value = getMetaProp($, propName);
	if (value) {
		meta[propName] = value;
	}
}
	

function extractMetaFromHtml(html) {
	const $ = cheerio.load(html);
  // console.log("Extracting og tags from html:\n");
	// console.log($.html());
	const title = getMetaProp($, 'title');
	if (title === null) {
		throw new NoMetadata({message: "No title prop"});
	}
	if (!title.length) {
		throw new InvalidMetadata({message: "Title prop cannot be empty"});
	}
	
	const type = getMetaPropOrThrowError($, 'type');
	const url = getMetaPropOrThrowError($, 'url');
	const image = getMetaPropOrThrowError($, 'image');
	const meta = new Meta({title, type, url, image});
	
	setMetaPropIfExists(meta, $, 'audio');
	setMetaPropIfExists(meta, $, 'description');
	setMetaPropIfExists(meta, $, 'determiner');
	setMetaPropIfExists(meta, $, 'locale');
	setMetaPropIfExists(meta, $, 'localeAlternate', 'locale:alternate');
	setMetaPropIfExists(meta, $, 'site_name');
	setMetaPropIfExists(meta, $, 'video');
	
	return meta
}

const server = thrift.createServer(MetaScrapper, {
  extractMetaFromUrl: function(url, result) {
    if (url.substring(0, 4) !== "http") {
    	url = "http://" + url;
    }	
  	console.log(`[GET] ${url}`);
  	fetchUrl(url, (error, meta, body) => {
  		if (error) {
  			console.error(`Error while fetching ${url}`);
  			console.log(error);
				result(new InvalidUrl({url, message: error.message || error}));
				return;
			}
			if (meta.status >= 400) {
			  console.error(meta.status);
				result(new InvalidUrl({url, message: `Status code is ${meta.status}`}));
				return;
			}
			try {
				const ogMeta = extractMetaFromHtml(body);
				result(null, ogMeta);
			} catch (e) {
			  if (e instanceof NoMetadata || e instanceof InvalidMetadata) {
  				result(e);
  				return;
				}
				throw e;
			}
		});
  }

});

console.log(`Listening on localhost:${port}`);
server.listen(port);
