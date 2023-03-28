import os
import re
import subprocess
from urllib.parse import quote

import pynvim

@pynvim.plugin
class ShareLinkPlugin(object):
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.command('ShareLink', nargs='*', sync=True)
    def share_link(self, args):
        file_path = self.nvim.eval('expand("%:p")')
        line_number = self.nvim.eval('line(".")')
        repo_root = subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'], encoding='utf-8'
        ).strip()

        os.chdir(repo_root)
        remote_url = subprocess.check_output(
            ['git', 'config', '--get', 'remote.origin.url'], encoding='utf-8'
        ).strip()

        if 'github.com' in remote_url:
            base_url = re.sub(r'\.git$', '', remote_url).replace(':', '/').replace('git@', 'https://')
            relative_path = os.path.relpath(file_path, repo_root)
            url = f"{base_url}/blob/master/{quote(relative_path)}#L{line_number}"
            self.nvim.command(f'echom "Link: {url}"')
        elif 'dev.azure.com' in remote_url:
            base_url = re.sub(r'\.git$', '', remote_url)
            relative_path = os.path.relpath(file_path, repo_root)
            url = f"{base_url}?path={quote(relative_path)}&version=GBmaster&_a=contents&line={line_number}&lineStyle=plain&lineEnd={line_number}&lineStartColumn=1&lineEndColumn=1"
            self.nvim.command(f'echom "Link: {url}"')
        else:
            self.nvim.command('echom "Error: Not a supported repository"')

