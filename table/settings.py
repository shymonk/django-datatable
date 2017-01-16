from django.conf import settings

TABLE_ATTR_ATTRS = getattr(settings, 'TABLE_ATTR_ATTRS', {})
# scrolling option
TABLE_ATTR_SCROLLABLE = getattr(settings, 'TABLE_ATTR_SCROLLABLE', False)
TABLE_ATTR_SCROLLINNER = getattr(settings, 'TABLE_ATTR_SCROLLINNER', "150%")
TABLE_ATTR_FIXED_COLUMNS = getattr(settings, 'TABLE_ATTR_FIXED_COLUMNS', None)
TABLE_ATTR_FIXED_COLUMNS_WIDTH = getattr(settings, 'TABLE_ATTR_FIXED_COLUMNS_WIDTH', None)
# sort
TABLE_ATTR_SEARCH = getattr(settings, 'TABLE_ATTR_SEARCH', True)
TABLE_ATTR_SEARCH_PLACEHOLDER = getattr(settings, 'TABLE_ATTR_SEARCH_PLACEHOLDER', None)

TABLE_ATTR_INFO = getattr(settings, 'TABLE_ATTR_INFO', True)
TABLE_ATTR_INFO_FORMAT = getattr(settings, 'TABLE_ATTR_INFO_FORMAT', None)

TABLE_ATTR_PAGINATION = getattr(settings, 'TABLE_ATTR_PAGINATION', True)
TABLE_ATTR_PAGE_LENGTH = getattr(settings, 'TABLE_ATTR_PAGE_LENGTH', 10)
TABLE_ATTR_PAGINATION_FIRST = getattr(settings, 'TABLE_ATTR_PAGINATION_FIRST', None)
TABLE_ATTR_PAGINATION_LAST = getattr(settings, 'TABLE_ATTR_PAGINATION_LAST', None)
TABLE_ATTR_PAGINATION_PREV = getattr(settings, 'TABLE_ATTR_PAGINATION_PREV', None)
TABLE_ATTR_PAGINATION_NEXT = getattr(settings, 'TABLE_ATTR_PAGINATION_NEXT', None)

TABLE_ATTR_LENGTH_MENU = getattr(settings, 'TABLE_ATTR_LENGTH_MENU', True)

TABLE_ATTR_EXT_BUTTON = getattr(settings, 'TABLE_ATTR_EXT_BUTTON', False)
TABLE_ATTR_EXT_BUTTON_TEMPLATE = getattr(settings, 'TABLE_ATTR_EXT_BUTTON_TEMPLATE', None)
TABLE_ATTR_EXT_BUTTON_TEMPLATE_NAME = getattr(settings, 'TABLE_ATTR_EXT_BUTTON_TEMPLATE_NAME', None)
TABLE_ATTR_EXT_BUTTON_CONTEXT = getattr(settings, 'TABLE_ATTR_EXT_BUTTON_CONTEXT', None)

TABLE_ATTR_ZERO_RECORDS = getattr(settings, 'TABLE_ATTR_ZERO_RECORDS', 'No records')
TABLE_ATTR_THEME_CSS_FILE = getattr(settings, 'TABLE_ATTR_THEME_CSS_FILE', 'table/css/datatable.bootstrap.css')
TABLE_ATTR_THEME_JS_FILE = getattr(settings, 'TABLE_ATTR_THEME_JS_FILE', 'table/js/bootstrap.dataTables.js')

TABLE_ATTR_MEDIA_JS = getattr(settings, 'TABLE_ATTR_MEDIA_JS', ('table/js/jquery.dataTables.min.js',
                                                                'table/js/jquery.browser.min.js',
                                                                'table/js/dataTables.fixedColumns.min.js'
                                                                ))  # option cutomize list of static to load
# option stateSave
TABLE_ATTR_STATESAVE = getattr(settings, 'TABLE_ATTR_STATESAVE', False)
TABLE_ATTR_STATEDURATION = getattr(settings, 'TABLE_ATTR_STATEDURATION', 604800)

# option language json
TABLE_ATTR_LANGUAGE_STATIC_JSON = getattr(settings, 'TABLE_ATTR_LANGUAGE_STATIC_JSON',
                                          'datatables/i18n/datatables.english.json')


TABLE_ATTR_DEFAULT_TIME_FORMAT = getattr(settings, 'TABLE_ATTR_DEFAULT_TIME_FORMAT',"%Y-%m-%d %H:%M:%S")