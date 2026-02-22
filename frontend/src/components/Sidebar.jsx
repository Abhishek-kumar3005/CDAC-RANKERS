import { Link, useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect, useRef } from "react";

import { AiOutlineMail, AiOutlineHome } from "react-icons/ai";
import { FiLogOut } from "react-icons/fi";
import {
  FaJava,
  FaPython,
  FaDatabase,
  FaCloud,
  FaRobot,
  FaChartBar,
  FaServer,
  FaProjectDiagram,
  FaRocket,
  FaBriefcase, // 👈 INTERVIEW ICON (BLACK)
} from "react-icons/fa";

export default function Sidebar() {
  const { pathname } = useLocation();
  const navigate = useNavigate();

  const [collapsed, setCollapsed] = useState(true);
  const [isMobile, setIsMobile] = useState(false);

  const sidebarRef = useRef(null);
  const toggleRef = useRef(null);

  /* ================= DETECT MOBILE ================= */
  useEffect(() => {
    const check = () => {
      const mobile = window.innerWidth <= 768;
      setIsMobile(mobile);
      if (mobile) setCollapsed(true);
    };

    check();
    window.addEventListener("resize", check);
    return () => window.removeEventListener("resize", check);
  }, []);

  /* ================= AUTO CLOSE ON ROUTE CHANGE (MOBILE) ================= */
  useEffect(() => {
    if (isMobile) setCollapsed(true);
  }, [pathname, isMobile]);

  /* ================= DESKTOP: CLOSE ON OUTSIDE CLICK ================= */
  useEffect(() => {
    if (isMobile) return;

    const handleOutsideClick = (e) => {
      if (
        !collapsed &&
        sidebarRef.current &&
        !sidebarRef.current.contains(e.target) &&
        toggleRef.current &&
        !toggleRef.current.contains(e.target)
      ) {
        setCollapsed(true);
      }
    };

    document.addEventListener("mousedown", handleOutsideClick);
    return () =>
      document.removeEventListener("mousedown", handleOutsideClick);
  }, [collapsed, isMobile]);

  /* ================= LOGOUT ================= */
  const handleLogout = () => {
    localStorage.removeItem("isLoggedIn");
    navigate("/", { replace: true });
  };

  /* ================= MODULES ================= */
  const modules = [
    { label: "Java", to: "/java", icon: <FaJava /> },
    { label: "Python", to: "/python", icon: <FaPython /> },
    { label: "Statistics", to: "/statistics", icon: <FaChartBar /> },
    { label: "DBMS", to: "/dbms", icon: <FaDatabase /> },
    { label: "Machine Learning", to: "/machinelearning", icon: <FaRobot /> },
    { label: "Data Visualisation", to: "/visualisation", icon: <FaProjectDiagram /> },
    { label: "Linux & Cloud", to: "/linuxcloud", icon: <FaCloud /> },
    { label: "Big Data", to: "/bigdata", icon: <FaServer /> },
  ];

  return (
    <>
      {/* ================= TOGGLE BUTTON ================= */}
      <button
        ref={toggleRef}
        onClick={() => setCollapsed(!collapsed)}
        style={{
          position: "fixed",
          top: "16px",
          left: isMobile ? "16px" : collapsed ? "16px" : "210px",
          width: "38px",
          height: "38px",
          borderRadius: "50%",
          background: "#fff",
          border: "1px solid #ddd",
          cursor: "pointer",
          zIndex: 3000,
        }}
      >
        {collapsed ? "☰" : "✕"}
      </button>

      {/* ================= MOBILE OVERLAY ================= */}
      {isMobile && !collapsed && (
        <div
          onClick={() => setCollapsed(true)}
          style={{
            position: "fixed",
            inset: 0,
            background: "rgba(0,0,0,0.4)",
            zIndex: 2000,
          }}
        />
      )}

      {/* ================= SIDEBAR ================= */}
      {(!isMobile || !collapsed) && (
        <aside
          ref={sidebarRef}
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: collapsed && !isMobile ? "70px" : "220px",
            height: "100vh",
            background: "#fff",
            borderRight: "1px solid #eee",
            transition: "0.35s cubic-bezier(.4,0,.2,1)",
            overflow: "hidden",
            zIndex: 2500,
            display: "flex",
            flexDirection: "column",
          }}
        >
          {/* ================= MODULES ================= */}
          <div style={{ marginTop: 80 }}>
            {!collapsed && (
              <div style={{ paddingLeft: 18, fontWeight: 600, marginBottom: 10 }}>
                DBDA Modules
              </div>
            )}

            {modules.map((item, i) => {
              const active = pathname === item.to;

              return (
                <Link
                  key={i}
                  to={item.to}
                  style={{
                    height: 42,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: collapsed && !isMobile ? "center" : "flex-start",
                    gap: 12,
                    paddingLeft: collapsed && !isMobile ? 0 : 18,
                    borderRadius: 8,
                    color: active ? "#007aff" : "#333",
                    background: active ? "#e8f0ff" : "transparent",
                    width: collapsed && !isMobile ? "48px" : "180px",
                    margin: "6px auto",
                    fontSize: 14,
                    textDecoration: "none",
                  }}
                >
                  {item.icon}
                  {!collapsed && item.label}
                </Link>
              );
            })}

            {/* ================= DBDA PROJECTS ================= */}
            <Link
              to="/projects"
              style={{
                height: 42,
                display: "flex",
                alignItems: "center",
                justifyContent: collapsed && !isMobile ? "center" : "flex-start",
                gap: 12,
                paddingLeft: collapsed && !isMobile ? 0 : 18,
                borderRadius: 8,
                color: pathname === "/projects" ? "#007aff" : "#333",
                background: pathname === "/projects" ? "#e8f0ff" : "transparent",
                width: collapsed && !isMobile ? "48px" : "180px",
                margin: "6px auto",
                fontSize: 14,
                fontWeight: 600,
                textDecoration: "none",
              }}
            >
              <FaRocket />
              {!collapsed && "DBDA Projects"}
            </Link>

            {/* ================= INTERVIEW SECTION (ADDED) ================= */}
            {!collapsed && (
              <div
                style={{
                  paddingLeft: 18,
                  fontWeight: 700,
                  marginTop: 14,
                  marginBottom: 6,
                  color: "#000",
                  fontSize: 13,
                }}
              >
                Interview
              </div>
            )}

            <Link
              to="/interview"
              style={{
                height: 42,
                display: "flex",
                alignItems: "center",
                justifyContent: collapsed && !isMobile ? "center" : "flex-start",
                gap: 12,
                paddingLeft: collapsed && !isMobile ? 0 : 18,
                borderRadius: 8,
                color: pathname === "/interview" ? "#000" : "#333",
                background: pathname === "/interview" ? "#f0f0f0" : "transparent",
                width: collapsed && !isMobile ? "48px" : "180px",
                margin: "6px auto",
                fontSize: 14,
                fontWeight: 600,
                textDecoration: "none",
              }}
            >
              <FaBriefcase color="#000" />
              {!collapsed && "Interview"}
            </Link>
          </div>

          {/* ================= FOOTER ================= */}
          <div style={{ marginTop: "auto", marginBottom: 30 }}>
            <Link
              to="/"
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: collapsed && !isMobile ? "center" : "flex-start",
                gap: 10,
                width: collapsed && !isMobile ? "48px" : "180px",
                paddingLeft: collapsed && !isMobile ? 0 : 18,
                height: 42,
                borderRadius: 8,
                textDecoration: "none",
                color: "#000",
                fontSize: 14,
                margin: "6px auto",
              }}
            >
              <AiOutlineHome size={20} />
              {!collapsed && "Home"}
            </Link>

            <Link
              to="/contact"
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: collapsed && !isMobile ? "center" : "flex-start",
                gap: 10,
                width: collapsed && !isMobile ? "48px" : "180px",
                paddingLeft: collapsed && !isMobile ? 0 : 18,
                height: 42,
                borderRadius: 8,
                textDecoration: "none",
                color: "#000",
                fontSize: 14,
                margin: "6px auto",
              }}
            >
              <AiOutlineMail size={20} />
              {!collapsed && "Contact"}
            </Link>

            <div
              onClick={handleLogout}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: collapsed && !isMobile ? "center" : "flex-start",
                gap: 10,
                width: collapsed && !isMobile ? "48px" : "180px",
                paddingLeft: collapsed && !isMobile ? 0 : 18,
                height: 42,
                borderRadius: 8,
                color: "red",
                fontSize: 14,
                cursor: "pointer",
                margin: "6px auto",
              }}
            >
              <FiLogOut size={20} />
              {!collapsed && "Logout"}
            </div>
          </div>
        </aside>
      )}
    </>
  );
}
