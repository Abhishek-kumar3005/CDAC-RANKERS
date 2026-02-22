import { Link } from "react-router-dom";
import { getAllArticles } from "../../utils/articles";
import "./article.css";

export default function Articles() {
  const articles = getAllArticles();

  return (
    <div className="article-wrapper">
      <h1>Articles</h1>

      <ul className="article-list">
        {articles.map((article) => (
          <li key={article.slug} className="article-item-row">
            <Link
              to={`/articles/${article.slug}`}
              className="article-link"
            >
              {article.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
