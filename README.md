# CreQQ
Lightweight and working API for fetching synchronized lyrics, powered by QQ Music.

```py
# Search for a song
queries = CreQQ().search('BLUE Billie Eilish')

# Get the metadata of the first song
metadata = queries[0].get_metadata()

# Print the 6th line of the lyrics
print(metadata.lyrics[5].raw)

# Output:
# [00:11.26]I try to live in black and white but I'm so blue
```

# Installation
Download the file [`creqq.py`](https://github.com/creuserr/creqq/blob/main/dist/creqq.py) and import it.

```py
from creqq import CreQQ
```

# Documentation

### class `CreQQ`
This class includes 3 subclasses and 1 method.

#### method `search(keyword: str) -> list`
This method searches for songs by the keyword. This will return a list of `CreQQ.Track` instances. Searched songs can be either the actual song, or a suggestion one. The maximum size of the list is strictly `10`.

```py
queries = CreQQ().search('BLUE Billie Eilish')
# Returns a list of CreQQ.Track instances
```

### class `CreQQ.Track`
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

### class `CreQQ.Metadata`
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

### class `CreQQ.Lyric`

This subclass is a single line of the track's lyrics including 3 properties&ndash;the timestamp (in milliseconds), text, and its raw value.

```py
print(lyrics[5].text)
# "I try to live in black and white but I'm so blue"

print(lyrics[5].timestamp)
# 11260

print(lyrics[5].raw)
# "[00:11.26]I try to live in black and white but I'm so blue"
```
