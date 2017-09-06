import json
import random
import string
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QAbstractScrollArea
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import qApp
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtWidgets import QSplitter
from PyQt5.QtWidgets import QStyleFactory
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget


class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):

        # ---------------------------------------------------------
        # ACTIONS
        # ---------------------------------------------------------

        # open
        open_act = QAction(QIcon('..\images\open.png'), '&Open', self)
        open_act.setShortcut('Ctrl+O')
        open_act.setStatusTip('Open a new HAR file')
        open_act.triggered.connect(self.showOpenDialog)
        
        #delete
        delete_act = QAction(QIcon('..\images\delete.png'), '&Delete', self)
        delete_act.setStatusTip('Delete the selected requests')
        delete_act.setShortcut('Delete')
        delete_act.triggered.connect(self.deleteRow)

        #expand
        expand_act = QAction(QIcon('..\images\expand.png'), 'E&xpand', self)
        expand_act.setStatusTip('Expand body')
        expand_act.setShortcut('Ctrl+X')
        expand_act.triggered.connect(self.expandBody)

        # quit
        exit_act = QAction(QIcon('..\images\exit.png'), '&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit Harshark')
        exit_act.triggered.connect(qApp.quit)
        
        # ---------------------------------------------------------
        # MENUBAR
        # ---------------------------------------------------------

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('&File')
        view_menu = menu_bar.addMenu('&View')
        options_menu = menu_bar.addMenu('&Options')

        file_menu.addAction(open_act)
        file_menu.addAction(exit_act)

        # ---------------------------------------------------------
        # TOOLBAR
        # ---------------------------------------------------------
        
        self.toolbar_actions = self.addToolBar('Useful commands')
        self.toolbar_search = self.addToolBar('Search & Filter')

        self.toolbar_search.setFloatable(False)
        self.toolbar_actions.setFloatable(False)

        self.toolbar_actions.addAction(open_act)
        self.toolbar_actions.addAction(delete_act)
        self.toolbar_actions.addAction(expand_act)
        
        searchbox = QLineEdit(self)
        searchbox_lbl = QLabel('Search Filter', self)
        searchbox_lbl.setMargin(5)
        searchbox.setPlaceholderText('Enter search query here to highlight matches')
        self.toolbar_search.addWidget(searchbox_lbl)
        self.toolbar_search.addWidget(searchbox)
        
        # ---------------------------------------------------------
        # STATUSBAR
        # ---------------------------------------------------------
        self.status_bar = self.statusBar()
        self.status_bar.showMessage('Ready')

        # ---------------------------------------------------------
        # REQUEST TABLE
        # ---------------------------------------------------------
        header_labels = ['id',
                        'Timestamp',
                        'Request Time',
                        'Server IP',
                        'Request Method',
                        'Request URL',
                        'Response Code',
                        'HTTP Version',
                        'Mime Type',
                        'Request Header Size',
                        'Request Body Size',
                        'Response Header Size',
                        'Response Body Size',
                        ]

        self.entry_table = QTableWidget()
        self.entry_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.entry_table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.entry_table.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.entry_table.setColumnCount(len(header_labels))
        self.entry_table.setHorizontalHeaderLabels(header_labels)
        self.entry_table.hideColumn(0)
        # when row clicked, fetch the request/response
        self.entry_table.itemSelectionChanged.connect(self.selectRow)

        # ---------------------------------------------------------
        # REQUESTS TAB
        # ---------------------------------------------------------

        request_tabs = QTabWidget()

        request_headers_tab = QWidget()
        request_body_tab = QWidget()
        request_query_tab = QWidget()
        request_cookie_tab = QWidget()

        request_tabs.addTab(request_headers_tab, 'Headers')
        request_tabs.addTab(request_body_tab, 'Body')
        request_tabs.addTab(request_query_tab, 'Query Strings')
        request_tabs.addTab(request_cookie_tab, 'Cookies')

        self.request_headers_tab_text = QTextEdit()
        self.request_body_tab_text = QTextEdit()
        self.request_query_tab_text = QTextEdit()
        self.request_cookie_tab_text = QTextEdit()

        self.request_headers_tab_text.setAcceptRichText(False)
        self.request_body_tab_text.setAcceptRichText(False)
        self.request_query_tab_text.setAcceptRichText(False)
        self.request_cookie_tab_text.setAcceptRichText(False)

        self.request_headers_tab_text.setReadOnly(True)
        self.request_body_tab_text.setReadOnly(True)
        self.request_query_tab_text.setReadOnly(True)
        self.request_cookie_tab_text.setReadOnly(True)

        self.request_headers_tab_text.setUndoRedoEnabled(False)
        self.request_body_tab_text.setUndoRedoEnabled(False)
        self.request_query_tab_text.setUndoRedoEnabled(False)
        self.request_cookie_tab_text.setUndoRedoEnabled(False)    
         
        request_headers_tab_layout = QVBoxLayout()
        request_body_tab_layout = QVBoxLayout()
        request_query_tab_layout = QVBoxLayout()
        request_cookie_tab_layout = QVBoxLayout()

        request_headers_tab_layout.addWidget(self.request_headers_tab_text)
        request_headers_tab.setLayout(request_headers_tab_layout)

        request_body_tab_layout.addWidget(self.request_body_tab_text)
        request_body_tab.setLayout(request_body_tab_layout)

        request_query_tab_layout.addWidget(self.request_query_tab_text)
        request_query_tab.setLayout(request_query_tab_layout)

        request_cookie_tab_layout.addWidget(self.request_cookie_tab_text)
        request_cookie_tab.setLayout(request_cookie_tab_layout)

        # ---------------------------------------------------------
        # RESPONSES TAB
        # ---------------------------------------------------------
        
        response_tabs = QTabWidget()

        response_headers_tab = QWidget()
        response_body_tab = QWidget()
        response_cookie_tab = QWidget()

        response_tabs.addTab(response_headers_tab, 'Headers')
        response_tabs.addTab(response_body_tab, 'Body')
        response_tabs.addTab(response_cookie_tab, 'Cookies')

        self.response_headers_tab_text = QTextEdit()
        self.response_body_tab_text = QTextEdit()
        self.response_cookie_tab_text = QTextEdit()

        self.response_headers_tab_text.setReadOnly(True)
        self.response_body_tab_text.setReadOnly(True)
        self.response_cookie_tab_text.setReadOnly(True)

        self.response_headers_tab_text.setAcceptRichText(False)
        self.response_body_tab_text.setAcceptRichText(False)
        self.response_cookie_tab_text.setAcceptRichText(False)

        self.response_headers_tab_text.setUndoRedoEnabled(False)
        self.response_body_tab_text.setUndoRedoEnabled(False)
        self.response_cookie_tab_text.setUndoRedoEnabled(False) 

        response_headers_tab_layout = QVBoxLayout()
        response_body_tab_layout = QVBoxLayout()
        response_cookie_tab_layout = QVBoxLayout()

        response_headers_tab_layout.addWidget(self.response_headers_tab_text)
        response_headers_tab.setLayout(response_headers_tab_layout)

        response_body_tab_layout.addWidget(self.response_body_tab_text)
        response_body_tab.setLayout(response_body_tab_layout)

        response_cookie_tab_layout.addWidget(self.response_cookie_tab_text)
        response_cookie_tab.setLayout(response_cookie_tab_layout)

        # ---------------------------------------------------------
        # GROUPBOX
        # ---------------------------------------------------------

        request_vbox = QVBoxLayout()
        response_vbox = QVBoxLayout()

        request_vbox.addWidget(request_tabs)
        response_vbox.addWidget(response_tabs)

        request_group_box = QGroupBox(title='Requests')
        request_group_box.setLayout(request_vbox)

        response_group_box = QGroupBox(title='Responses')
        response_group_box.setLayout(response_vbox)

        # ---------------------------------------------------------
        # WIDGET SPLITTER
        # ---------------------------------------------------------

        splitter_hor = QSplitter(Qt.Horizontal)
        splitter_hor.addWidget(request_group_box)
        splitter_hor.addWidget(response_group_box)

        splitter_ver = QSplitter(Qt.Vertical)
        splitter_ver.addWidget(self.entry_table)
        splitter_ver.addWidget(splitter_hor)

        self.setCentralWidget(splitter_ver)

        # ---------------------------------------------------------
        # MAIN
        # ---------------------------------------------------------
        
        self.showMaximized()
        # app title
        self.setWindowTitle('Harshark | HTTP Archive (HAR) Viewer | v0.2')
        # app icon
        self.setWindowIcon(QIcon('..\images\logo2.png'))
        # display the app
        self.show()

    def deleteRow(self):
        """delete the selected rows from the requests table when hitting the 
        'delete' key
        """
        all_selection_groups = self.entry_table.selectedRanges()
        # count number of row selection groups
        number_of_selection_groups = len(all_selection_groups)
        # for each row selection group
        for i in range(number_of_selection_groups, 0, -1):
            # index into this row selection group
            selRange  = all_selection_groups[number_of_selection_groups - 1]
            # get first row for this selection
            fist_row = selRange.topRow()
            # get last row for this selection
            last_row = selRange.bottomRow()
            # delete from first to last row in this selection        
            for j in range(last_row, fist_row - 1, -1):
                self.entry_table.removeRow(j)
            # decrement, to move to next row selection group
            number_of_selection_groups -= 1


    def harParse(self, archive):

        # remove any previous entries
        self.entry_table.setRowCount(0)
        
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximumWidth(300)
        self.progress_bar.setMaximumHeight(17)
        self.status_bar.clearMessage()
        self.status_bar.addWidget(self.progress_bar)

        try:
            with open(archive, encoding='utf-8') as har:
                har = json.load(har)
        except json.decoder.JSONDecodeError:
            self.status_bar.removeWidget(self.progress_bar)
            self.status_bar.showMessage('Invalid file')
            return

        self.request_headers_dict = {}
        self.request_body_dict = {}
        self.request_cookies_dict = {}
        self.request_queries_dict = {}
        self.response_headers_dict = {}
        self.response_body_dict = {}
        self.response_cookies_dict = {}
        
        for i, entry in enumerate(har['log']['entries']):

            # occasionally update the import progress bar
            if i % 10 == 0:
                QApplication.processEvents()
                self.progress_bar.setValue(i / len(har['log']['entries']) * 100)

            # unique ID for each request for lookups
            id = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
            
            row_data = []
            row_data.append(id)
            try:
                row_data.append(entry['startedDateTime'])
            except KeyError:
                row_data.append('')
            try:
                row_data.append(entry['time'])
            except KeyError:
                row_data.append('')
            try:
                row_data.append(entry['serverIPAddress'])
            except KeyError:
                row_data.append('')
            try:
                row_data.append(entry['request']['method'])
            except KeyError:
                row_data.append('')
            try:                   
                row_data.append(entry['request']['url'])
            except KeyError:
                row_data.append('')
            try:
                row_data.append(entry['response']['status'])
            except KeyError:
                row_data.append('')
            try:
                row_data.append(entry['response']['httpVersion'])
            except KeyError:
                row_data.append('')
            try:
                row_data.append(entry['response']['content']['mimeType'])
            except KeyError:
                row_data.append('')
            try:
                row_data.append(entry['request']['headersSize'])
            except KeyError:
                row_data.append('')
            try:                
                row_data.append(entry['request']['bodySize'])
            except KeyError:
                row_data.append('')
            try:                
                row_data.append(entry['response']['headersSize'])
            except KeyError:
                row_data.append('')
            try:
                row_data.append(entry['response']['bodySize'])
            except KeyError:
                row_data.append('')                

            # populate the entries table
            self.entry_table.insertRow(i)
            for j, item in enumerate(row_data):
                self.entry_table.setItem(i, j, QTableWidgetItem(str(item)))
            
            # fill the requests dictionaries
            try:
                self.request_headers_dict[id] = entry['request']['headers']
            except KeyError:
                self.request_headers_dict[id] = ' No request headers found'
            try:
                self.request_body_dict[id] = entry['request']['postData']
            except KeyError:
                self.request_body_dict[id] = ''
            try:
                self.request_cookies_dict[id] = entry['request']['cookies']
            except KeyError:
                self.request_cookies_dict[id] = ''
            try:
                self.request_queries_dict[id] = entry['request']['queryString']
            except KeyError:
                self.request_queries_dict[id] =''

            # fill the response dictionaries
            try:
                self.response_headers_dict[id] = entry['response']['headers']
            except KeyError:
                self.response_headers_dict[id] = 'No response headers found'
            try:
                self.response_body_dict[id] = entry['response']['content']
            except KeyError:
                self.response_body_dict[id] = ''
            try:
                self.response_cookies_dict[id] = entry['response']['cookies']
            except:
                self.response_cookies_dict[id] = ''

        # resize to entries table
        self.entry_table.resizeColumnsToContents()
        # overwrite URL column sizing
        self.entry_table.setColumnWidth(5, 800)
        
        # update the statusbar on success
        self.progress_bar.setValue(100)
        self.status_bar.removeWidget(self.progress_bar)
        self.status_bar.showMessage('HAR imported sucessfully')
        
    def selectRow(self):

        truncate_size = 2000

        body_safelist = [
                'text', 
                'html',
                'css',
                'json',
                'javascript',
                'js',
                'xml'
        ]

        cookie_list = []

        self.request_headers_tab_text.setPlainText('')
        self.request_body_tab_text.setPlainText('')
        self.request_query_tab_text.setPlainText('')
        self.request_cookie_tab_text.setPlainText('')
        self.response_headers_tab_text.setPlainText('')
        self.response_body_tab_text.setPlainText('')
        self.response_cookie_tab_text.setPlainText('')

        # all rows have been deleted
        if self.entry_table.currentRow() == -1:
            return

        row_id = self.entry_table.item(self.entry_table.currentRow(), 0).text()
        
        request_headers = self.request_headers_dict[row_id]
        request_body = self.request_body_dict[row_id]
        request_cookies = self.request_cookies_dict[row_id]
        request_queries = self.request_queries_dict[row_id]
        response_headers = self.response_headers_dict[row_id]
        response_body = self.response_body_dict[row_id]
        response_cookies = self.response_cookies_dict[row_id]

        for item in request_headers:
            entry = '<p><b>{}</b><br>{}'.format(item['name'], item['value'])
            self.request_headers_tab_text.append(str(entry))

        if request_body != '':
            if any(mime in request_body['mimeType'] for mime in body_safelist):
                try:
                    entry = request_body['text']
                    self.request_body_tab_text.insertPlainText(str(entry))
                except KeyError:
                    self.request_body_tab_text.insertPlainText('No request body found')
            elif request_body['mimeType'] == '':
                self.request_body_tab_text.insertPlainText('')
            else:
                self.request_body_tab_text.insertPlainText('Non ASCII request')  
        else:
            self.request_body_tab_text.insertPlainText('')  
        
        for item in request_queries:
            entry = '<p>     <b>{}</b><br>{}'.format(item['name'], item['value'])
            self.request_query_tab_text.append(str(entry))
        
        for item in request_cookies:
            entry = '<p>     <b>{}</b><br>{}'.format(item['name'], item['value'])
            self.request_cookie_tab_text.append(str(entry))

        # parse response headers
        for item in response_headers:

            # display response headers
            entry = '<b>{}</b><br>{}<br>'.format(item['name'], item['value'])
            self.response_headers_tab_text.append(str(entry))

            # parse 'set-cookie header in response header if we don't have them 
            # in nice HAR format
            if not response_cookies:
                if item['name'] == 'Set-Cookie' or item['name'] == 'set-cookie':
                    cookie_header = item['value'].split('\n')
                    for cookie in cookie_header:
                        this_cookie = cookie.split(';')
                        for each in this_cookie:
                            self.response_cookie_tab_text.append(each.strip())
                        self.response_cookie_tab_text.append('')

        # parse response body

        if response_body != '':
            if any(mime in response_body['mimeType'] for mime in body_safelist):
                try:
                    entry = response_body['text'][:truncate_size]
                    if len(entry) == truncate_size:
                        entry = '---BODY TRUNCATED--- (Ctrl+X to expand)\n\n' + str(entry)
                    self.response_body_tab_text.insertPlainText(entry)
                except KeyError:
                    self.response_body_tab_text.insertPlainText('No response body found')
            else:
                self.response_body_tab_text.insertPlainText('Non ASCII response')
        else:
            self.response_body_tab_text.insertPlainText('No response body found')
    
        # parse response cookies

        if response_cookies:
            for item in response_cookies:
                
                cookie = {'name':'',
                    'value':'',
                    'path':'',
                    'domain':'',
                    'expires':'',
                    'httpOnly':'',
                    'secure':'' 
                    }

                try:
                    cookie['name'] = item['name']
                except KeyError:
                    pass
                try:
                    cookie['value'] = item['value']
                except KeyError:
                    pass
                try:
                    cookie['path'] = item['path']
                except KeyError:
                    pass
                try:
                    cookie['domain'] = item['domain']
                except KeyError:
                    pass
                try:
                    cookie['expires'] = item['expires']
                except KeyError:
                    pass
                try:
                    cookie['httpOnly'] = item['httpOnly']
                except KeyError:
                    pass
                try:
                    cookie['secure'] = item['secure']
                except KeyError:
                    pass

                cookie_list.append(cookie)

            for cookie in cookie_list:
                entry = '''<b>Name</b>: {}<br>
                            <b>Value</b>: {}<br>
                            <b>Path</b>: {}<br>
                            <b>Domain</b>: {}<br>
                            <b>Expires</b>: {}<br>
                            <b>httpOnly</b>: {}<br>
                            <b>Secure</b>: {}<br>'''.format(
                                cookie['name'], cookie['value'], cookie['path'],
                                cookie['domain'], cookie['expires'], cookie['httpOnly'],
                                cookie['secure'])

                self.response_cookie_tab_text.append(entry)

    def expandBody(self):

        # if all rows have been removed from entries table do nothing
        if self.entry_table.currentRow() == -1:
            return

        # get row id
        row_id = self.entry_table.item(self.entry_table.currentRow(), 0).text()
        # get current body text
        body_text = self.response_body_tab_text.toPlainText()

        # show full response body if we know it's been truncated
        if '---BODY TRUNCATED---' in body_text:
            response_body = self.response_body_dict[row_id]
            entry = str(response_body['text'])
            self.response_body_tab_text.setPlainText('')
            self.response_body_tab_text.insertPlainText(entry)
        
        return

    def showOpenDialog(self):
        file_name = QFileDialog.getOpenFileName(self, 'Open file')
        har = file_name[0]
        # no file selected
        if har == '':
            return()
        # parse the HAR file
        self.harParse(har)


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont('Segoe UI', 10))
    app.setStyle("Fusion")
    main_harshark = MainApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()