import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux'
import PropTypes from 'prop-types'


import { ADMIN_URL } from '../constants'

class Page extends React.Component {
    constructor(props) {
        super(props);
        this.state = { showSource: false };
        this.toggleSource = this.toggleSource.bind(this);
    }

    componentDidUpdate() {
        window.scrollTo(0, 0);
    }

    getMarkdownText(markdown) {
        const rawMarkup = markdown ? marked(markdown): '';
        return {__html: rawMarkup};
    }

    toggleSource() {
        const showSource = !this.state.showSource;
        this.setState({ ...this.state, showSource });
    }

    render() {
        const page = this.props.page;

        if (!page) {
            return (
                <div>
                    <Header />
                    <div id="content">
                        <p>Loading...</p>
                        <Link to="/">ahernp.com</Link>
                    </div>
                    <Footer />
                </div>
            );
        }

        const generateChildLinks = (currentPage) => {
            let childLinks = [];
            if (page.id) {
                const children = this.props.pages.filter(page => page.parent_id === currentPage.id);
                if (children.length) {
                    childLinks = children.map(page =>
                        <Link key={page.id} to={'/pages/' + page.slug}>{page.title}</Link>
                    ).reduce((prev, curr) => [prev, ' ', curr]);
                }
            }
            return childLinks;
        };

        const childLinks = generateChildLinks(page);

        const source = <div id="page-source">
                        <h2>Page Source</h2>
                        <pre>{page.content}</pre>
                    </div>;

        return (
            <React.Fragment>
                <Header page={page} />
                <div id="content">
                    <h2>{page.title}</h2>
                    <p>{childLinks}</p>
                    <div dangerouslySetInnerHTML={this.getMarkdownText(page.content)}></div>
                    {this.state.showSource && source}
                </div>
                <Footer>
                    <span>Updated <FormatDate dateString={page.updated}/></span>{' '}
                    <a href={ADMIN_URL + '/pages/page/' + page.id}>Admin</a>{' '}
                    <Link to="/pages/markdown">Markdown</Link>{' '}
                    <span className="ap-control" onClick={this.toggleSource}>Source</span>
                </Footer>
            </React.Fragment>
        )
    }
}

Page.propTypes = {
  page: PropTypes.object,
  pages: PropTypes.array.isRequired
};

function mapStateToProps(state, props) {
    const slug = props.match.params.slug;
    const page = state.pagesReducer.find(page => page.slug === slug);
    return {
        pages: state.pagesReducer,
        page
    };
}

export default connect(
  mapStateToProps,
  null
)(Page);
