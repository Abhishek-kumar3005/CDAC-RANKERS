import { useState } from "react";

export default function DBDAPracticeTests() {
  const [open, setOpen] = useState(false);

  const tests = [
    ...Array.from({ length: 10 }, (_, i) => `Practice Test ${i + 1}`),
    "Final 100 MCQ",
    "CCEE Previous Years",
  ];

  return (
    <>
      {/* ===== Desktop Sidebar ===== */}
      <aside className="dbda-practice desktop-only">
        <h3>Practice Tests</h3>
        {tests.map((t, i) => (
          <div className="practice-item" key={i}>{t}</div>
        ))}
      </aside>

      {/* ===== Mobile Button ===== */}
      <button className="practice-mobile-btn" onClick={() => setOpen(true)}>
        📋 Practice Tests
      </button>

      {/* ===== Mobile Drawer ===== */}
      {open && (
        <div className="practice-drawer-overlay" onClick={() => setOpen(false)}>
          <div
            className="practice-drawer"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="drawer-header">
              <h3>Practice Tests</h3>
              <button className="drawer-close" onClick={() => setOpen(false)}>
                ✕
              </button>
            </div>

            {tests.map((t, i) => (
              <div className="practice-item" key={i}>{t}</div>
            ))}
          </div>
        </div>
      )}
    </>
  );
}