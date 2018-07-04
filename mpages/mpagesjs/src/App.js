import axios from "axios";

import React, { Component } from "react";

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

const API_URL_PAGES = "/api/v1/pages/";
const API_URL_CONTENT_AS_HTML = "/api/v1/markdown-to-html";

class App extends Component {
    constructor(props) {
        super(props);
        const pageId = window.page_id;
        this.state = { pageId, content: "", content_as_html: "" };
        this.onChange = this.onChange.bind(this);
        this.savePage = this.savePage.bind(this);
        this.updatePreview = this.updatePreview.bind(this);
    }
 
    async componentDidMount() {
        const { pageId } = this.state;
        const response = await axios.get(API_URL_PAGES + pageId);
        const { content, content_as_html } = response.data;
        this.setState({ content, content_as_html });
    }


    onChange(e) {
        this.setState({ ...this.state, [e.target.name]: e.target.value });
    }

    async savePage(e) {
        const { pageId } = this.state;
        const newContent = this.state.content;
        const response = await axios.put(
            API_URL_PAGES + pageId + "/",
            {
                id: pageId,
                content: newContent
            });
        const { content, content_as_html } = response.data;
        this.setState({ content, content_as_html });
    };

    async updatePreview(e) {
        const content = e.target.value;
        const response = await axios.post(
            API_URL_CONTENT_AS_HTML,
            { content });
        const content_as_html = response.data;
        this.setState({ content, content_as_html });
    };

    render() {
        const { content, content_as_html } = this.state;
        return (
            <React.Fragment>
                <button onClick={this.savePage}>Save</button>
                <div id="markdown">
                    <textarea name="content" value={content} onChange={this.onChange} onBlur={this.updatePreview}></textarea>
                </div>
                <div id="preview" dangerouslySetInnerHTML={{__html: content_as_html}}>
                </div>
            </React.Fragment>
        );
    }
}

export default App;
