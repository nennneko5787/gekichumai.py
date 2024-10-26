import random
import string


class Utils:
    @classmethod
    def random_string(cls, n: int) -> str:
        """n文字分のランダムな文字列を生成します。

        Args:
            n (int): 文字数

        Returns:
            str: ランダムな文字列。
        """
        return "".join(random.choices(string.ascii_letters + string.digits, k=n))
