import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import DBDAModuleLayout from "../../components/DBDAModuleLayout";
import "./dbdaLayout.css";

export default function MachineLearning() {
  const [content, setContent] = useState("");
  const [activeTest, setActiveTest] = useState(null);

  // 🔹 Mobile drawer state
  const [showDrawer, setShowDrawer] = useState(false);

  useEffect(() => {
    if (activeTest === null) {
      fetch("/content/notes/machinelearning.md")
        .then((res) => res.text())
        .then(setContent);
    } else {
      fetch(`/content/tests/machinelearning/test ${activeTest}.md`)
        .then((res) => res.text())
        .then(setContent);
    }
  }, [activeTest]);

  return (
    <DBDAModuleLayout title="Machine Learning">
      <div className="dbda-layout">
        {/* ================= MAIN CONTENT ================= */}
        <section className="dbda-section dbda-main">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {content}
          </ReactMarkdown>
        </section>

        {/* ================= PRACTICE TEST SIDEBAR (DESKTOP) ================= */}
        <aside className="dbda-practice desktop-only">
          <h3>Practice Tests</h3>

          {[1, 2, 3, 4, 5, 6, 7, 8].map((num) => (
            <div
              key={num}
              className="practice-item"
              onClick={() => setActiveTest(num)}
            >
              Practice Test {num}
            </div>
          ))}

          <div
            className="practice-item"
            style={{ marginTop: "20px", color: "#555" }}
            onClick={() => setActiveTest(null)}
          >
            ← Back to Notes
          </div>
        </aside>
      </div>

      {/* ================= MOBILE TESTS BUTTON ================= */}
      <button
        className="practice-mobile-btn"
        onClick={() => setShowDrawer(true)}
      >
        Tests
      </button>

      {/* ================= MOBILE TEST DRAWER ================= */}
      {showDrawer && (
        <div
          className="practice-drawer-overlay"
          onClick={() => setShowDrawer(false)}
        >
          <div
            className="practice-drawer"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="drawer-header">
              <h3>Practice Tests</h3>
              <button
                className="drawer-close"
                onClick={() => setShowDrawer(false)}
              >
                ✕
              </button>
            </div>

            {[1, 2, 3, 4, 5, 6, 7, 8].map((num) => (
              <div
                key={num}
                className="practice-item"
                onClick={() => {
                  setActiveTest(num);
                  setShowDrawer(false);
                }}
              >
                Practice Test {num}
              </div>
            ))}

            <div
              className="practice-item"
              style={{ marginTop: "20px", color: "#555" }}
              onClick={() => {
                setActiveTest(null);
                setShowDrawer(false);
              }}
            >
              ← Back to Notes
            </div>
          </div>
        </div>
      )}
    </DBDAModuleLayout>
  );
}
