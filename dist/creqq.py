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
    
    def get_metadata(self):
      h = { 'Referer': 'y.qq.com/portal/player.html' }
      res = requests.get('https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?songmid=' + self.id + '&g_tk=5381', headers=h)
      text = res.text
      parsed = json.loads(text[18:len(text) - 1])
      return CreQQ.Metadata(base64.b64decode(str.encode(parsed['lyric'])).decode('utf-8'))
  
  class Lyric:
    def __init__(self, min, sec, line):
      self.raw = f'[{min}:{sec}]{line}'
      self.text = line
      self.timestamp = int(min) * 60
      self.timestamp += float(sec)
      self.timestamp *= 1000
      self.timestamp = int(self.timestamp)
  
  class Metadata:
    def __init__(self, raw):
      self.raw = raw
      self.entries = []
      self.title = None
      self.artist = None
      self.album = None
      self.lyrics = []
      lines = raw.split('\n')
      for line in lines:
        entry = self._entry(line)
        if entry == None: continue
        entype = self._entype(entry[0])
        enval = self._enval(entry[0])
        if entype == 'ti':
          self.title = enval
        elif entype == 'al':
          self.album = enval
        elif entype == 'ar':
          self.artist = enval
        elif entype == 'offset':
          self.offset = float(enval)
        elif entype.isnumeric():
          self.lyrics.append(CreQQ.Lyric(entype, enval, entry[1]))
        self.entries.append(entry)
    
    def _entype(self, raw):
      m = re.search(r'\[.*?\:', raw)
      end = m.end()
      return raw[1:end - 1]
    
    def _enval(self, raw):
      m = re.search(r'\[.*?\:', raw)
      end = m.end()
      return raw[end:len(raw) - 1]
    
    def _entry(self, raw):
      m = re.search(r'\[.*?\:.*?\]', raw)
      if m == None: return
      end = m.end()
      key = raw[0:end]
      value = raw[end:]
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
