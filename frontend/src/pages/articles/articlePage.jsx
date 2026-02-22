import { useParams, useNavigate } from "react-router-dom";
import { getAllArticles } from "../../utils/articles";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./article.css";

export default function ArticlePage() {
  const { slug } = useParams();
  const navigate = useNavigate();

  const articles = getAllArticles();
  const article = articles.find((a) => a.slug === slug);

  if (!article) {
    return <div className="article-wrapper">Article not found.</div>;
  }

  return (
    <div className="article-wrapper">

      {/* 🔙 BACK BUTTON */}
      <button
        className="back-button"
        onClick={() => navigate("/articles")}
      >
        ← Back to Articles
      </button>

      <h1>{article.title}</h1>

      <div className="article-content">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>
          {article.content}
        </ReactMarkdown>
      </div>

    </div>
  );
}
