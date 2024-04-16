"""
pip install を自動でする
"""

from typing import Any, Dict, Union, Optional
from subprocess import check_output
from pip._internal.cli.main import main as _main
from importlib import import_module
from json import loads


class ImportCheck:
    """
    自動pipクラス
    """

    def __init__(self, *, debug: bool = False) -> None:
        self._importList = []
        self._updateList = []
        self._insCB = False
        self._updCB = False

        self.debug = debug

        self.importData = self._ImportData()

    def get_packageData(self, packageName: str) -> Union[Dict[str, str], bool]:
        """
        pip install されているか確認
        """
        for l in self._importList:
            if l["name"] == packageName:
                return l
        return False

    def updatePip(self, packageName: str, *, over: bool = False, obligation: bool = False) -> bool:
        """
        pip install -U を実行
        """
        self._updateListCheck()
        if obligation:
            try:
                if over:
                    check_output(
                        f"python -m pip install --upgrade {packageName}")
                else:
                    _main(['install', '-U', packageName])
                return True
            except:
                pass
            return False

        if self.get_packageData(packageName):
            try:
                for l in self._updateList:
                    if l["name"] == packageName:
                        if over:
                            check_output(
                                f"python -m pip install --upgrade {packageName}")
                        else:
                            _main(['install', '-U', packageName])
                        break
                return True
            except Exception:
                if self.debug:
                    print(f"{packageName}のpip install -Uに失敗しました")
        elif self.debug:
            print(f"{packageName}はinstallされていません！")
        return False

    def loadPip(self, packageName: str) -> bool:
        """
        pip install を実行
        """
        self._installListCheck()
        if self.get_packageData(packageName):
            if self.debug:
                print(f"{packageName}は既にinstallされています！")
            return True
        else:
            try:
                _main(['install', packageName])
                return True
            except Exception:
                if self.debug:
                    print(f"{packageName}のpip installに失敗しました")
        return False

    def loadImport(self, packageName: str, name: Optional[str] = None) -> bool:
        """
        import ~~~ as ~~~
        を実行
        """
        if name == None:
            name = packageName
        try:
            self.importData._add(name, import_module(packageName))
            return True
        except Exception:
            if self.debug:
                print(f"{packageName}のimportに失敗しました")
        return False

    def _installListCheck(self) -> None:
        """
        installListが既にpip installされているか確認し、
        既にpip installされていない場合はinstallする
        """
        if self._insCB:
            return
        self._insCB = True
        try:
            self._importList = loads(check_output("pip3 list --format json"))
        except Exception as e:
            if self.debug:
                print("pip install list load Error!\n", e)

    def _updateListCheck(self) -> None:
        if self._updCB:
            return
        self._updCB = True
        try:
            self._updateList = loads(
                check_output("pip3 list -o --format json"))
        except Exception as e:
            if self.debug:
                print("pip update list load Error!\n", e)

    class _ImportData:
        def _add(self, key: str, value: Any) -> None:
            setattr(self, key, value)

        def __getitem__(self, key) -> Any:
            try:
                return getattr(self, key)
            except Exception:
                pass
            return None
