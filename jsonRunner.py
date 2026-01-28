"""
Extends JsonFunk to be able to run entries as commands,
filling in placeholders in {} brackets with json members.

Normally this would be an intermediary tool used by a derived class.
The idea is the child class would do something like:
    def foo(self,variable):
        self._runCommand("foo",variable=variable)
"""
import typing
import subprocess
from .jsonFunk import JsonFunk


class JsonRunner(JsonFunk):
    """
    Extends JsonFunk to be able to run entries as commands,
    filling in placeholders in {} brackets with json members.

    Normally this would be an intermediary tool used by a derived class.
    The idea is the child class would do something like:
        def foo(self,variable):
            self._runCommand("foo",variable=variable)
    """

    def _runCommand(self,commandNameInJsonObj:str,**otherVars)->str:
        """
        Run a command by replacing the placeholders with
        the values from self.jsonObj and otherVars

        Returns the command line output
        """
        replacements:typing.Dict[str,typing.Any]={}
        replacements.update(self.jsonObj)
        replacements.update(otherVars)
        cmda:typing.List[str]=[]
        for cmdPart in self.jsonObj[commandNameInJsonObj].split('{'):
            if not cmda:
                cmda.append(cmdPart)
            else:
                repl,after=cmdPart.rsplit('}',1)
                repl=str(getattr(self,repl))
                cmda.append(after)
        cmd=''.join(cmda)
        print(cmd)
        po=subprocess.Popen(cmd,
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        out,_=po.communicate()
        if isinstance(out,bytes):
            ret=out.decode('UTF-8',errors="ignore")
        else:
            ret=out
        contents=str(ret).strip().replace('\r','')
        return f"$> {cmd}\n{contents}"

    def __call__(self,commandNameInJsonObj:str,**otherVars)->str:
        """
        This class can be called like a function.

        (Though derived classes should probably not depend on this
        and instead call _runCommand() )
        """
        return self._runCommand(commandNameInJsonObj,**otherVars)
