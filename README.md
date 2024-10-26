# gekichumai.py

ゲキチュウマイ-NET を Python から利用できるモジュール。

## Current Limits

### 以下の機能は実装できていません

- オンゲキ(今度プレイする予定です)
- スタンダードコース / オンゲキプレミアムコース の機能

## How to install the gekichumai.py

以下のコマンドを実行してください。

```
(Windows)
py -m pip install git+https://github.com/nennneko5787/gekichumai.py

(Mac / Linux)
python3 -m pip install git+https://github.com/nennneko5787/gekichumai.py
```

## Examples

### Chunithm

#### sync_chunithm.py

```python
from gekichumai import Chunithm

client = Chunithm()


def main():
    client.login("segaid here", "password here")
    print(client.gamedata)
    # [GameData(idx=0, icon='https://new.chunithm-net.com/chuni-mobile/html/mobile/img/184a8273ecedc0e9.png', honor='お菓子をくれないと悪戯しちゃうｿﾞ☆(≧▽≦)／', level=2, name='ＮＥＮＮＮＥＫＯ', rating=3.92, max_rating=3.92, over_power=432.58, over_power_percentage=0.39, lastplaydate=datetime.datetime(2024, 10, 26, 15, 56))]


main()
```
