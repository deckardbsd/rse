from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms import validators

from index import Searcher
from lang_proc import query_terms


app = Flask(__name__)
Bootstrap(app)
# TODO make it configurable
searcher = Searcher('/tmp/indexed_docs/')


class SearchForm(Form):
    uquery = StringField('User Query:', validators=[validators.DataRequired()])
    sbutton = SubmitField('Search')

@app.route('/', methods=['GET', 'POST'])
def index():
    search_form = SearchForm(csrf_enabled=False)
    if search_form.validate_on_submit():
        return redirect(url_for('search_results', query=search_form.uquery.data))
    return render_template('index.html', form=search_form)

@app.route('/search_results/<query>')
def search_results(query):
    query_words = query.split(' ')
    # query_words = query_terms(query)
    print('Query words ----------- {}'.format(query_words))
    doc_ids = searcher.find_documents_AND(query_words)
    urls = [searcher.get_url(id) for id in doc_ids]
    print 'URLS len is {}'.format(len(urls))
    # texts = [" ".join(searcher.get_document_text(id)) for id in doc_ids]
    texts = [" ".join(searcher.get_snippet(query_words, id)) for id in doc_ids]
    return render_template('search_results.html', query=query, urls=urls, texts_and_urls=zip(urls, texts))

if __name__ == '__main__':
    app.run(debug=True)
