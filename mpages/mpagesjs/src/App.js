import axios from "axios";

import React, { Component } from "react";

const API_URL_PAGES = "/api/v1/pages/";
const API_URL_CONTENT_AS_HTML = "/api/v1/markdown-to-html/";

class App extends Component {
    constructor(props) {
        super(props);
        const pageId = window.page_id;
        console.log("PageId", pageId);
        this.state = { pageId, page: {content: "", content_as_html: ""} };
        this.updatePreview = this.updatePreview.bind(this);
    }
 
    async componentDidMount() {
        const { pageId } = this.state;
        const response = await axios.get(API_URL_PAGES + pageId);
        this.setState({ page: response.data });
    }

    async updatePage(content) {
        const { pageId } = this.state;
        const response = await axios.post(
            API_URL_PAGES + pageId,
            {
                id: pageId,
                content: content
            });
        this.setState({ page: response.data });
    };

    async updatePreview(content) {
        const response = await axios.post(
            API_URL_CONTENT_AS_HTML,
            { content });
        let { page } = this.state;
        page.content = content;
        page.content_as_html = response.data;
        this.setState({ page });
    };

    render() {
        const { page } = this.state;
        return (
            <React.Fragment>
                <div id="markdown">
					<textarea src={page.content}></textarea>
                </div>
                <div id="preview">
                    {page.content_as_html}
                </div>
            </React.Fragment>
        );
    }
}

export default App;
