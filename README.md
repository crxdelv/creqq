# CreQQ
Lightweight and working API for fetching synchronized lyrics, powered by QQ Music.

```py
# Search for a song
queries = CreQQ().search('BLUE Billie Eilish')

# Get the metadata of the first song
metadata = queries[0].get_metadata()

# Print the 2nd line of the lyrics
print(metadata.lyrics[1].raw)

# Output:
# [00:11.26]I try to live in black and white but I'm so blue
```

# Installation
Download the file [`creqq.py`](https://github.com/creuserr/creqq/blob/main/dist/creqq.py) and import it.

```py
from creqq import CreQQ
```

> [!NOTE]
> This library uses the dependency `requests`.

# REST API

```http
GET https://creqq-api.vercel.app/<SEARCH-QUERY>/<SEARCH-INDEX>
```

[Try it online!](https://reqbin.com/1umgymx1)

## Parameters

**Search Query** <br>
This is the search query for searching the song lyrics. It is recommended to also include the artist name for precise result.h

**Search Index** <br>
When searching, it can return a bunch of songs. Search index is used to select which song to return. It is zero by default and can be undefined.

***

`offset` is the offset start of the lyrics by seconds. If the offset is 2 seconds, then you need to manually adjust the lyrics.

`total` is the total amount of songs that has been retrieved when searching.

`index` is the number of which song index is returned. It is basically search index but with +1.

`timestamp` is the milliseconds timestamp of a lyric line.

## Response Schema

### 200 Success
```http
GET https://creqq-api.vercel.app/i%20can%20see%20you%20taylor

{
  "title": "I Can See You (Taylor's Version|From The Vault)",
  "artist": "Taylor Swift",
  "offset": 0,
  "total": 10,
  "index": 0,
  "lyrics": [{
      "timestamp": 16470,
      "text": "You brush past me in the hallway"
  }, "..."],
  "success": true
}
```

### 400 Bad Request

`INCOMPLETE_PARAM` occurs if no parameter is provided.
```http
GET https://creqq-api.vercel.app/
{
  "error": "INCOMPLETE_PARAM"
  "success": false
}
```

`INVALID_PARAM` occurs if the search index is not a valid number.
```http
GET https://creqq-api.vercel.app/i%20can%20see%20you%20taylor/not-a-number

{
  "error": "INVALID_PARAM"
  "success": false
}
```

### 404 Not Found

`NOT_FOUND` occurs when either the search query doesn't return a single song, or the index is out of bounds.
```http
GET https://creqq-api.vercel.app/gajsjsjauwhsja

{
  "error": "NOT_FOUND"
  "success": false
}
```

`NO_METADATA_FOUND` occurs when a song exists but doesn't have a lyrics.

> [!NOTE]
> The metadata includes all the data including the title and the artist.

```http
GET https://creqq-api.vercel.app/i%20can%20see%20you%20taylor/3
{
  "error": "NO_METADATA_FOUND"
  "success": false
}
```

### 500 Internal Error

`INTERNAL_ERROR` occurs when the process raised an error.
```json
{
  "error": "INTERNAL_ERROR",
  "message": "...",
  "traceback": "...",
  "success": false
}
```

# Documentation

## class `CreQQ`
This class includes 3 subclasses and 1 method.

#### method `search(keyword: str) -> list`
This method searches for songs by the keyword. This will return a list of `CreQQ.Track` instances. Searched songs can be either the actual song, or a suggestion one. The maximum size of the list is strictly `10`.

```py
queries = CreQQ().search('BLUE Billie Eilish')
# Returns a list of CreQQ.Track instances
```

## class `CreQQ.Track`
This subclass includes 1 method, and 3 properties&ndash;the track title, album name, and the artist name. 

```py
print(queries[0].title)
# "BLUE"

print(queries[0].artist)
# "Billie Eilish"

print(queries[0].album)
# "HIT ME HARD AND SOFT"
```

#### method `get_metadata() -> CreQQ.Metadata`

This method will return the metadata of the track.

```py
metadata = queries[0].get_metadata()
# Returns an instance of CreQQ.Metadata
```

## class `CreQQ.Metadata`
This subclass is just like the `CreQQ.Track` class, but with additional properties&ndash;the lyrics and the offset value (in seconds).

> [!NOTE]
> Properties of `CreQQ.Track` and `CreQQ.Metadata` (title, artist, album) can be different. Tracks are inherited from the API's information while metadata are inherited from the Lyrics' information.

```py
print(metadata.title)
# "BLUE"

print(metadata.artist)
# "Billie Eilish"

print(metadata.album)
# "HIT ME HARD AND SOFT"

print(metadata.offset)
# 0.0

lyrics = metadata.lyrics
# Returns a list of CreQQ.Lyric instances
```

`metadata.lyrics` is a lyrically-ordered list of `CreQQ.Lyric` instances.

## class `CreQQ.Lyric`

This subclass is a single line of the track's lyrics including 3 properties&ndash;the timestamp (in milliseconds), text, and its raw value.

```py
print(lyrics[1].text)
# "I try to live in black and white but I'm so blue"

print(lyrics[1].timestamp)
# 11260

print(lyrics[1].raw)
# "[00:11.26]I try to live in black and white but I'm so blue"
```

<img src="https://komarev.com/ghpvc/?username=creuserr" alt="" width="0"></img>
