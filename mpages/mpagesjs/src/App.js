import axios from "axios";

import React, { Component } from "react";

const API_URL_PAGES = "/api/v1/pages/";

class App extends Component {
    constructor(props) {
        super(props);
        const pageId = window.page_id;
        const response = await axios.get(API_URL_PAGES + pageId);
        this.state = { page: response.data };
        this.updatePreview = this.updatePreview.bind(this);
    }
 
    updatePreview() {
        const response = await axios.post(
            API_URL_PAGES + pageId,
            {
                id: page.id,
                content: page.content
            });
        this.setState({ page: response.data });
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
