from __future__ import unicode_literals

import click

__version__ = '0.0.1'
click.disable_unicode_literals_warning = True

contents = '''ADD_NEW_LINE_AT_END_OF_FILE: true
AUTOPEP8_PARAMETERS: ''
BLANK_LINES_INNER: 1
BLANK_LINES_TOP_LEVEL: 2
BREAK_IMPORTS_MODE: PARENTHESIS
DATE_FIELD_FORMAT: yyyy-MM-dd
DATE_FIELD_NAME: __updated__
DELETE_UNUSED_IMPORTS: false
ENABLE_DATE_FIELD_ACTION: false
FORMAT_BEFORE_SAVING: true
FORMAT_ONLY_CHANGED_LINES: false
FORMAT_WITH_AUTOPEP8: false
FROM_IMPORTS_FIRST: false
GROUP_IMPORTS: true
IMPORT_ENGINE: IMPORT_ENGINE_ISORT
MANAGE_BLANK_LINES: true
MULTILINE_IMPORTS: true
SAVE_ACTIONS_ONLY_ON_WORKSPACE_FILES: true
SORT_IMPORTS_ON_SAVE: true
SORT_NAMES_GROUPED: true
SPACES_BEFORE_COMMENT: '2'
SPACES_IN_START_COMMENT: '1'
TRIM_EMPTY_LINES: true
TRIM_MULTILINE_LITERALS: true
USE_ASSIGN_WITH_PACES_INSIDER_PARENTESIS: false
USE_OPERATORS_WITH_SPACE: true
USE_SPACE_AFTER_COMMA: true
USE_SPACE_FOR_PARENTESIS: false
'''.replace('\r\n', '\n').replace('\r', '\n').encode('utf-8')


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(version=__version__)
@click.argument(
    'source',
    nargs=-1,
    type=click.Path(
        exists=True, file_okay=True, dir_okay=True, readable=True, allow_dash=True
    ),
    is_eager=True,
)
@click.pass_context
def main(ctx, source=None):
    from functools import partial
    import os
    import io

    out = partial(click.secho, bold=True, err=True)
    err = partial(click.secho, fg='red', err=True)

    if not source:
        out('No directories passed. Nothing to do.')
        ctx.exit(0)

    for entry in source:
        for root, dirs, files in os.walk(entry):
            if 'tasks.py' in files:
                target = os.path.join(root, 'tasks.py')
                with io.open(target, 'r', encoding='utf-8') as stream:
                    if 'hooks' not in stream.read():
                        err('Did not find hooks in: %s' % (target,))

            for directory in dirs:
                if os.path.exists(os.path.join(root, directory, '.pydevproject')):
                    # Ok, found a .pydevproject, so, we have to set the
                    # new settings to be used.
                    settings_dir = os.path.join(root, directory, '.settings')
                    if not os.path.exists(settings_dir):
                        os.makedirs(settings_dir)
                    target = os.path.join(settings_dir, 'org.python.pydev.yaml')
                    if os.path.exists(target):
                        out('Updating: %s' % (target,))
                    else:
                        out('Creating: %s' % (target,))
                    with io.open(target, 'wb') as stream:
                        stream.write(contents)

    out('Finished')
    ctx.exit(0)


if __name__ == '__main__':
    main()
