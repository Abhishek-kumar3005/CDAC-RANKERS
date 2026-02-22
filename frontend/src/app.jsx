import { Routes, Route, useLocation } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import Contact from "./pages/Contact";
import Home from "./pages/Home";
import Caption from "./pages/projects/Caption";
import OCR from "./pages/projects/OCR";
import ObjectDetect from "./pages/projects/ObjectDetect";
import Emotion from "./pages/projects/Emotion";
import Photoshop from "./pages/projects/Photoshop";
import CatDog from "./pages/projects/CatDog";
import Java from "./pages/DBDA/Java";
import LinuxCloud from "./pages/DBDA/linuxcloud";
import Python from "./pages/DBDA/python";
import Visualisation from "./pages/DBDA/visualisation";
import MachineLearning from "./pages/DBDA/machinelearning";
import Statistics from "./pages/DBDA/statistics";
import BigData from "./pages/DBDA/bigdata";
import Landing from "./pages/Landing";
import DBMS from "./pages/DBDA/dbms";
import Projects from "./pages/projects/Projects";
import InterviewModule from "./pages/Interview/InterviewModule";
import Javainterview from "./pages/Interview/Javainterview";
import Pythoninterview from "./pages/Interview/Pythoninterview";
import Sqlinterview from "./pages/Interview/Sqlinterview";
import Bigdatainterview from "./pages/Interview/Bigdatainterview";
import Cloudinterview from "./pages/Interview/Cloudinterview";
import Machinelearninginterview from "./pages/Interview/Machinelearninginterview";
import Statisticsinterview from "./pages/Interview/Statisticsinterview";
import Visualisationinterview from "./pages/Interview/Visualisationinterview";
import Pythonlogicinterview from "./pages/Interview/Pythonlogicinterview";
import Sqlqueriesinterview from "./pages/Interview/Sqlqueriesinterview";
import Cloudessentialsinterview from "./pages/Interview/Cloudessentialsinterview";
import Hrinterview from "./pages/Interview/Hrinterview";
import Articles from "./pages/articles/articles";
import ArticlePage from "./pages/articles/articlePage";





import CaptionDocs from "./pages/docs/CaptionDocs";



export default function App() {
  const location = useLocation();


  const hideSidebar = location.pathname === "/landing";

  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        width: "100vw",
        overflow: "hidden",
        position: "relative",
      }}
    >
      {!hideSidebar && <Sidebar />}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          overflowX: "hidden",
          padding: hideSidebar ? "0px" : "30px",
          background: "linear-gradient(to bottom right, #f9fbff, #e9f2ff)",
          position: "relative",
          zIndex: 10,
        }}
      >
        <Routes>
          <Route path="/landing" element={<Landing />} />
          <Route path="/" element={<Home />} />
          <Route path="/caption" element={<Caption />} />
          <Route path="/ocr" element={<OCR />} />
          <Route path="/detect" element={<ObjectDetect />} />
          <Route path="/emotion" element={<Emotion />} />
          <Route path="/photoshop" element={<Photoshop />} />
          <Route path="/catdog" element={<CatDog />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/java" element={<Java />} />
          <Route path="/linuxcloud" element={<LinuxCloud />} />
          <Route path="/python" element={<Python />} />
          <Route path="/visualisation" element={<Visualisation />} />
          <Route path="/machinelearning" element={<MachineLearning />} />
          <Route path="/statistics" element={<Statistics />} />
          <Route path="/bigdata" element={<BigData />} />
          <Route path="/dbms" element={<DBMS />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/interview" element={<InterviewModule />} />
          <Route path="/interview/java" element={<Javainterview />} />
          <Route path="/interview/python" element={<Pythoninterview />} />
          <Route path="/interview/statistics" element={<Statisticsinterview />} />
          <Route path="/interview/dbms" element={<Sqlinterview />} />
          <Route path="/interview/ml" element={<Machinelearninginterview />} />
          <Route path="/interview/visualisation" element={<Visualisationinterview />} />
          <Route path="/interview/cloud" element={<Cloudinterview />} />
          <Route path="/interview/bigdata" element={<Bigdatainterview />} />
          <Route path="/interview/python-logics" element={<Pythonlogicinterview />} />
          <Route path="/interview/sql-queries" element={<Sqlqueriesinterview />} />
          <Route path="/interview/cloud-essentials" element={<Cloudessentialsinterview />} />
          <Route path="/interview/Hrinterview" element={<Hrinterview />} />
          <Route path="/articles" element={<Articles />} />
          <Route path="/articles/:slug" element={<ArticlePage />} />

          <Route path="/docs/caption" element={<CaptionDocs />} />
        </Routes>
      </div>
    </div>
  );
}
