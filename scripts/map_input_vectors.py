import ast
import os
import sys
import json

class CommandStructureVisitor(ast.NodeVisitor):
    def __init__(self):
        # Map variable names to their node info
        # { var_name: { 'type': 'parser'|'subparsers', 'name': 'cmd_name', 'parent': parent_var_name } }
        self.vars = {'parser': {'type': 'parser', 'name': 'ROOT', 'parent': None}}
        self.commands = {} # Flat list of discovered commands with args: { 'cmd_path': [args] }
        
    def get_cmd_path(self, var_name):
        path = []
        curr = var_name
        while curr and curr in self.vars:
            info = self.vars[curr]
            if info['name'] and info['name'] != 'ROOT':
                path.insert(0, info['name'])
            curr = info['parent']
        return " ".join(path)

    def visit_Assign(self, node):
        # Handle assignments like: watch_p = subparsers.add_parser("watch")
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute):
            method = node.value.func.attr
            caller = node.value.func.value.id if isinstance(node.value.func.value, ast.Name) else None
            
            if not caller: 
                return

            # parser.add_subparsers
            if method == 'add_subparsers':
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.vars[target.id] = {'type': 'subparsers', 'name': None, 'parent': caller}
            
            # subparsers.add_parser("name")
            elif method == 'add_parser':
                if node.value.args and isinstance(node.value.args[0], ast.Constant):
                    cmd_name = node.value.args[0].value
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            # caller is the subparsers var, its parent is the parser var
                            parent_parser = self.vars.get(caller, {}).get('parent')
                            self.vars[target.id] = {'type': 'parser', 'name': cmd_name, 'parent': parent_parser}
                            
                            # Initialize command entry
                            full_path = self.get_cmd_path(target.id)
                            if full_path not in self.commands:
                                self.commands[full_path] = []

    def visit_Call(self, node):
        # Handle direct calls without assignment: watch_sub.add_parser("start")
        if isinstance(node.func, ast.Attribute):
            method = node.func.attr
            
            # Case 1: Caller is a variable (e.g. parser.add_argument)
            if isinstance(node.func.value, ast.Name):
                caller = node.func.value.id
                if caller not in self.vars:
                    return

                # .add_parser("name") (without assignment)
                if method == 'add_parser':
                    if node.args and isinstance(node.args[0], ast.Constant):
                        cmd_name = node.args[0].value
                        # caller is the subparsers group
                        parent_group = self.vars.get(caller)
                        parent_cmd_var = parent_group.get('parent') if parent_group else None
                        
                        parent_path = self.get_cmd_path(parent_cmd_var)
                        full_path = (parent_path + " " + cmd_name).strip()
                        
                        if full_path not in self.commands:
                            self.commands[full_path] = []

                # .add_argument("--arg")
                elif method == 'add_argument':
                    # If multiple args (e.g. -f, --file), get all
                    args = []
                    for a in node.args:
                        if isinstance(a, ast.Constant):
                            args.append(a.value)
                    
                    full_path = self.get_cmd_path(caller)
                    if full_path not in self.commands:
                        self.commands[full_path] = []
                    
                    if args:
                        self.commands[full_path].append(", ".join(args))

            # Case 2: Chained call (e.g. sub.add_parser("cmd").add_argument("--arg"))
            elif isinstance(node.func.value, ast.Call):
                inner_call = node.func.value
                if isinstance(inner_call.func, ast.Attribute) and inner_call.func.attr == 'add_parser':
                    if inner_call.args and isinstance(inner_call.args[0], ast.Constant):
                        cmd_name = inner_call.args[0].value
                        
                        if isinstance(inner_call.func.value, ast.Name):
                            parent_var = inner_call.func.value.id
                            parent_group = self.vars.get(parent_var)
                            parent_cmd_var = parent_group.get('parent') if parent_group else None
                            
                            parent_path = self.get_cmd_path(parent_cmd_var)
                            full_path = (parent_path + " " + cmd_name).strip()
                            
                            if method == 'add_argument':
                                args = [a.value for a in node.args if isinstance(a, ast.Constant)]
                                if full_path not in self.commands:
                                    self.commands[full_path] = []
                                if args:
                                    self.commands[full_path].append(", ".join(args))

def map_vectors(filepath):
    with open(filepath, "r") as f:
        tree = ast.parse(f.read())
    
    visitor = CommandStructureVisitor()
    visitor.visit(tree)
    
    print("# CLIDE Input Vectors Map")
    print("\n| Command | Arguments |")
    print("| :--- | :--- |")
    
    # Sort by command path length (groups root commands together)
    for cmd, args in sorted(visitor.commands.items()):
        arg_str = "<br>".join(args) if args else "(none)"
        print(f"| `{cmd}` | {arg_str} |")

if __name__ == "__main__":
    target = "clide/serve/portal.py"
    if len(sys.argv) > 1:
        target = sys.argv[1]
    
    if os.path.exists(target):
        map_vectors(target)
    else:
        print(f"Error: {target} not found")
