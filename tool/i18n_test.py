import glob
import re
import os
import json
import datetime

# タグの正規表現パターン
tag_pattern = re.compile('\$t\(\'[^\']*?\'')

# 文字エンコーディング
ENCODING = 'UTF-8'

# 出力ファイル設定
OUTPUT_DIR = 'auto-i18n'
JSON_FILE_NAME_SUFFIX = '.i18n.json'
DATETIME_FORMAT = '%Y%m%d%H%M%S'
TEST_RESULT = 'result_' + datetime.datetime.now().strftime(DATETIME_FORMAT) + '.csv'

# チェックするディレクトリのリスト
CHECK_DIR = ['pages', 'components']

# 言語のリスト
# 1番目に書かれた言語をデフォルト言語（Vueファイル内に記載されている言語，タグ名となる）として処理します
LANG = ['ja', 'en', 'ja-basic']

# auto-i18n/に自動生成ファイルを出力するか
AUTO_GEN = False

# タグ総数
total = 0

# エラーの数
error_count = 0

# 警告の数
warn_count = 0

# チェックされたファイルの数
file_count = 0

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
        tags = [tag[4:(len(tag) - 1)] for tag in tag_pattern.findall(content)]

        # json生成用辞書
        tags_dict = json.loads('{}')
        for lang in LANG:
          tags_dict[lang] = {}

        for tag in tags:
          # 辞書に追加
          if(len(tag) > 0):
            for lang in LANG:
              tags_dict[lang][tag] = tag if lang == LANG[0] else ''

        # テスト対象のjsonのパス
        json_path = os.path.join(os.path.dirname(path), os.path.splitext(os.path.basename(path))[0] + JSON_FILE_NAME_SUFFIX)

        # テスト用にauto-i18n/に出力
        if(AUTO_GEN):
          with open(os.path.join(cdir, OUTPUT_DIR, os.path.basename(path)) + JSON_FILE_NAME_SUFFIX, mode='w', encoding=ENCODING) as i18n:
            # json出力
            json.dump(tags_dict, i18n, ensure_ascii=False, indent=2)

        total += len(tags)

        # json内のtagと照合
        if(os.path.exists(json_path)):
          with open(json_path, encoding=ENCODING) as test_file:
            test_json = json.load(test_file)
            for lang in tags_dict:
              # 言語が不足
              if(lang not in test_json):
                test_result.write(','.join(['LANG', json_path, lang]) + '\n')
                error_count += 1
                continue
              # タグチェック
              for tag in tags_dict[lang]:
                # タグが存在する場合未翻訳のチェック
                if(tag in test_json[lang]):
                  if(lang != LANG[0] and test_json[lang][tag] == ''):
                    print('WARN: ' + tag + ' (' + lang + ') may not be translated')
                    warn_count += 1
                    test_result.write(','.join(['WARN', json_path, tag + ' (' + lang + ')']) + '\n')
                # タグが不足
                else:
                  print('TAG: ' + tag + ' (' + lang + ' ) does not exists in ' + json_path)
                  error_count += 1
                  test_result.write(','.join(['TAG', json_path, tag + ' (' + lang + ')']) + '\n')
        # ファイルが不足
        else:
          test_result.write(','.join(['FILE', json_path, '']) + '\n')
          error_count += 1

# タグ総数出力（言語ごとに別のタグとして数える）
print('total : ' + str(total * len(LANG)))
# エラー数出力
print('error : ' + str(error_count))
# 警告数出力
print('warn : ' + str(warn_count))
# ファイル総数出力
print('checked file: ' + str(file_count))