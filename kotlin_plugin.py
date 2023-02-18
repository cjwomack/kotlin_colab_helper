import subprocess
import os
from IPython.core.magic import Magics, cell_magic, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
from pygments import highlight
from pygments.lexers import KotlinLexer
#import pygments.lexers
#import pygments.formatters
from pygments.formatters import HtmlFormatter
from IPython.display import display, HTML

def print_out(out: str):
    for l in out.split('\n'):
        print(l)

def displayHTML(html_code):
    '''
    Display HTML in notebook
    '''
    display(HTML(html_code))

@magics_class
class KotlinLex(Magics):
    @staticmethod
    def compile(src, out):
        #compiler = 'g++'
        #compiler = f"/content/kotlinc/bin/kotlinc {src} -include-runtime -d /content/{out}.jar; java -jar /content/{out}.jar"
        compiler = "/content/kotlinc/bin/kotlinc"
        res = subprocess.check_output(
            [compiler, src, "-include-runtime", "-d", f"/content/{out}.jar"], stderr=subprocess.STDOUT)
        print_out(res.decode("utf8"))
        res2 = subprocess.check_output(
         ["java", "-jar", f"/content/{out}.jar"], stderr=subprocess.STDOUT)
        print_out(res2.decode("utf8"))
        #/content/kotlinc/bin/kotlinc {filename}.kt -include-runtime -d /content/{filename}.jar; java -jar /content/{filename}.jar"

    @staticmethod
    def custom_compile(arg_list):
        res = subprocess.check_output(
            arg_list, stderr=subprocess.STDOUT)
        print_out(res.decode("utf8"))

    @magic_arguments()
    @argument('-n', '--name', type=str, help='File name that will be produced by the cell.')
    @argument('-c', '--compile', type=str, help='Compile command. Use true for default command or specify command in single quotes.')
    @argument('-a', '--append', help='Should be appended to same file', action="store_true")
    @argument('-s', '--style', type=str, help='Pygments style name')
    @cell_magic
    def run_kt(self, line='', cell=None):
        '''
        C++ syntax highlighting cell magic.
        '''
        global style
        args = parse_argstring(self.run_kt, line)
        if args.name != None:
            ex = args.name.split('.')[-1]
            if ex not in ['kt','kts']:
                raise Exception('Name must end with .kt or .kts')
        else:
            args.name = 'src.kt'

        if args.append:
            mode = "a"
        else:
            mode = "w"
    
        with open(args.name, mode) as f:
            f.write(cell)

        if args.style == None:
            displayHTML(highlight(cell, KotlinLexer(), HtmlFormatter(full=True,nobackground=True,style='paraiso-light')))
        else:
            displayHTML(highlight(cell, KotlinLexer(), HtmlFormatter(full=True,nobackground=True,style=args.style)))

        if args.compile != None:
            try:
                print("-*"*30)
                displayHTML("* <b>O U T P U T</b>")
                print("-*"*30,end="")
                if args.compile == 'true':
                    self.compile(args.name, args.name.split('.')[0])
                else:
                    self.custom_compile(args.compile.replace("'", "").split(' '))
            except subprocess.CalledProcessError as e:
                print_out(e.output.decode("utf8"))

def load_ipython_extension(ip):
    os.system('pip install pygments ipywidgets')
    plugin = KotlinLex(ip)
    ip.register_magics(plugin)
