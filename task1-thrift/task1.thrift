struct Meta {
  1: string title,
  2: optional string type,
  3: optional string image,
  4: optional string url,
  5: optional string audio,
	6: optional string description,
  7: optional string determiner,
  8: optional string locale,
  9: optional string localeAlternate,
  10: optional string site_name,
  11: optional string video
}

exception InvalidUrl {
  1: string url,
	2: optional string message
}

exception NoMetadata {
  1: optional string message
}

exception InvalidMetadata {
  1: string message
}

service MetaScrapper {
  Meta extractMetaFromUrl(1:string html) throws (1:InvalidUrl invalidUrlException, 2:NoMetadata noMetadataException, 3:InvalidMetadata invalidMetadataException)
}
