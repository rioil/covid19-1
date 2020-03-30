import glob
import re
import os
import json
import datetime
import pathlib

# チェックするディレクトリのリスト
CHECK_DIR = ['pages', 'components']

# 言語のリスト
# 1番目に書かれた言語をデフォルト言語（Vueファイル内に記載されている言語，タグ名となる）として処理します
LANG = ['ja', 'en', 'ja-basic']

# タグの正規表現パターン
tag_pattern = re.compile('\$t\(\'[^\']*?\'')

# 文字エンコーディング
ENCODING = 'UTF-8'

# 出力ファイル設定
OUTPUT_DIR = 'auto-i18n'
JSON_FILE_NAME_SUFFIX = '.i18n.json'
DATETIME_FORMAT = '%Y%m%d%H%M%S'
TEST_RESULT = 'result_' + datetime.datetime.now().strftime(DATETIME_FORMAT) + '.csv'

# タグ総数
total = 0

# エラーの数
error_count = 0

# 警告の数
warn_count = 0

# チェックされたファイルの数
file_count = 0

def check_json(tags: dict, json: dict, set_value: bool, path: str, lang: str, fp) -> dict:
  if(not isinstance(tags, dict)):
    return {}
  for k, v in tags.items():
    if(isinstance(v, dict)):
      if(k not in json):
        json[k] = {}
        fp.write(','.join(['TAG', path, k + ' (' + lang + ')']) + '\n')
        print('Add TAG: ' + k + ' to ' + path)
      json[k] = check_json(v, json[k], set_value, path, lang, fp)
    else:
      if(k not in json):
        json[k] = k if set_value else ''
        fp.write(','.join(['TAG', path, k + ' (' + lang + ')']) + '\n')
        print('Add TAG: ' + k + ' to ' + path)
      elif(json[k] == ''):
        fp.write(','.join(['WARN', path, k + ' (' + lang + ')']) + '\n')
        print('WARN: ' + k + ' (' + lang + ') in ' + path)
  return json

#####処理部開始#####
# ディレクトリ毎にテスト
for cdir in CHECK_DIR:
  # リポジトリのルートからのパスをtoolからの相対パスに変換
  cdir = os.path.join(os.pardir, cdir)
  # 自動生成json出力フォルダ作成
  os.makedirs(os.path.join(cdir, OUTPUT_DIR), exist_ok=True)
  # すべてのVueファイルを検索
  vue_files = (glob.glob(cdir + os.sep + '**' + os.sep + '*.vue', recursive=True))
  file_count += len(vue_files)

  with open(os.path.join(cdir, OUTPUT_DIR, TEST_RESULT), mode='w', encoding=ENCODING) as test_result:
    # 各Vueファイルについて処理
    for path in vue_files:
      with open(path, encoding=ENCODING) as file:
        # ファイルの内容を文字列として取得
        content = ''.join([l.strip() for l in file])
        # 全タグを正規表現で取得
        tags = {}
        for raw_tag in [tag[4:(len(tag) - 1)] for tag in tag_pattern.findall(content)]:
          if(len(raw_tag) <= 0): continue
          nest_struct = raw_tag.split('.')
          nest = 'tags'

          for i in range(len(nest_struct)):
            if(nest_struct[i] not in eval(nest).keys()):
              nest += ('["' + nest_struct[i] + '"]')
              exec(nest + ' = {}')
            else:
              nest += ('["' + nest_struct[i] + '"]')
          exec(nest + ' = ""')

        total += len(tags)

        json_path = os.path.join(os.path.dirname(path), os.path.splitext(os.path.basename(path))[0] + JSON_FILE_NAME_SUFFIX)
        cur_json = {}
        p_cur_json = pathlib.Path(json_path)

        # jsonファイルが存在しなければ空ファイル作成
        if(not p_cur_json.exists()):
          p_cur_json.touch()

        # 現在のjsonをチェックし不足するタグを追加
        with p_cur_json.open(mode='r', encoding=ENCODING) as cur_file:
          try:
            cur_json = json.load(cur_file)
          except json.JSONDecodeError:
            print('INVALID FORMAT: ' + json_path)
            test_result.write(','.join(['FILE', json_path, '']) + '\n')

          for lang in LANG:
            # 言語のチェック
            if(lang not in cur_json):
              print('Add LANG: ' + lang + ' to ' + json_path)
              cur_json[lang] = {}
              test_result.write(','.join(['LANG', json_path, lang]) + '\n')
            # タグのチェック
            cur_json[lang] = check_json(tags, cur_json[lang], lang == LANG[0], json_path, lang, test_result)

        # チェック後のjsonを保存
        with p_cur_json.open(mode='w', encoding=ENCODING) as cur_file:
          json.dump(cur_json, cur_file, ensure_ascii=False, indent=4)

# タグ総数出力（言語ごとに別のタグとして数える）
print('total : ' + str(total * len(LANG)))
# エラー数出力
# print('error : ' + str(error_count))
# 警告数出力
# print('warn : ' + str(warn_count))
# ファイル総数出力
print('checked file: ' + str(file_count))