import requests
import base64
import json
import re

class CreQQ:
  class Track:
    def __init__(self, parsed):
      self.id = parsed['songmid']
      self.title = parsed['songname']
      self.album = parsed['albumname']
      self.artist = parsed['singer'][0]['name']
    
    def get_lyrics(self):
      h = { 'Referer': 'y.qq.com/portal/player.html' }
      res = requests.get('https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?songmid=' + self.id + '&g_tk=5381', headers=h)
      text = res.text
      parsed = json.loads(text[18:len(text) - 1])
      return CreQQ.Lyrics(base64.b64decode(str.encode(parsed['lyric'])).decode('utf-8'))
  
  class Lyrics:
    def __init__(self, raw):
      self.raw = raw
      self.entries = []
      self.title = None
      self.artist = None
      self.album = None
      lines = raw.split('\n')
      for line in lines:
        entry = self._entry(line)
        entype = self._entype(entry[0])
        enval = self._enval(entry[0])
        print(entype)
        if entype == 'ti':
          pass
        self.entries.append(entry)
    
    def _entype(self, raw):
      end = re.search(r'\[.*?\:', raw).end()
      return raw[1:end - 1]
    
    def _enval(self, raw):
      end = re.search(r'\[.*?\:', raw).end()
      return raw[end:len(raw) - 1]
    
    def _entry(self, raw):
      end = re.search(r'\[.*?\:.*?\]', raw).end()
      key = raw[0:end]
      value = raw[end:len(raw)]
      return [key, value]
  
  def search(self, term):
    res = requests.get('https://c.y.qq.com/soso/fcgi-bin/client_search_cp?w=' + term)
    text = res.text
    parsed = json.loads(text[9:len(text) - 1])
    tracklist = parsed['data']['song']['list']
    res = []
    for track in tracklist:
      res.append(CreQQ.Track(track))
    return res
