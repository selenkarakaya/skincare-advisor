// // import { useState } from "react";
// // import axios from "axios";

// // function App() {
// //   const [problem, setProblem] = useState("");
// //   const [recommendations, setRecommendations] = useState([]);
// //   const [ingredients, setIngredients] = useState([]);
// //   const [warnings, setWarnings] = useState("");
// //   const [avoid, setAvoid] = useState([]);
// //   const [loading, setLoading] = useState(false);

// //   const handleSubmit = async (e) => {
// //     e.preventDefault();
// //     setLoading(true);
// //     setRecommendations([]);
// //     setIngredients([]);
// //     setAvoid([]);
// //     setWarnings("");

// //     try {
// //       const response = await axios.post(
// //         "http://127.0.0.1:8000/api/recommend/",
// //         { problem }
// //       );
// //       console.log("response.data:", response.data);
// //       console.log("recommendations:", response.data.recommendations);
// //       console.log("warnings", response.data.warning_message);
// //       console.log("ingredients", response.data.ingredients);

// //       setRecommendations(response.data.recommendations);
// //       setWarnings(response.data.warning_message);
// //       setIngredients(response.data.ingredients);
// //       setAvoid(response.data.avoid);
// //     } catch (error) {
// //       console.error("Error fetching recommendations:", error);
// //     }

// //     setLoading(false);
// //   };

// //   return (
// //     <div className="container">
// //       <h1>Skincare Advisor</h1>
// //       <form onSubmit={handleSubmit}>
// //         <textarea
// //           value={problem}
// //           onChange={(e) => setProblem(e.target.value)}
// //           placeholder="Describe your skin problem..."
// //         />
// //         <button type="submit" disabled={loading}>
// //           {loading ? "Analyzing..." : "Get Advice"}
// //         </button>
// //       </form>

// //       {recommendations.length > 0 && (
// //         <div>
// //           <h2>Recommendations:</h2>
// //           <ul>
// //             {recommendations.map((rec, index) => (
// //               <li key={index}>{rec}</li>
// //             ))}
// //           </ul>
// //         </div>
// //       )}
// //       {ingredients.length > 0 && (
// //         <div>
// //           <h2>ingredients:</h2>
// //           <ul>
// //             {ingredients.map((rec, index) => (
// //               <li key={index}>{rec}</li>
// //             ))}
// //           </ul>
// //         </div>
// //       )}
// //       <p>{avoid.join(", ")}</p>

// //       {warnings && (
// //         <div
// //           style={{
// //             whiteSpace: "pre-line", // Satır sonlarını ve boşlukları korur
// //             padding: "20px", // Tüm kenarlara 20px padding ekler
// //             backgroundColor: "#f8d7da", // Arka plan rengi (isteğe bağlı)
// //             border: "1px solid #f5c6cb", // Kenar rengi (isteğe bağlı)
// //             borderRadius: "5px", // Kenarları yuvarlatmak (isteğe bağlı)
// //           }}
// //           dangerouslySetInnerHTML={{
// //             __html: warnings,
// //           }}
// //         />
// //       )}
// //       {/* {warnings.length > 0 && (
// //         <div className="warnings">
// //           <h2>Warning:</h2>
// //           <ul>
// //             {warnings.map((warning, index) => (
// //               <li key={index} className="warning-message">
// //                 {warning}
// //               </li>
// //             ))}
// //           </ul>
// //         </div>
// //       )} */}
// //     </div>
// //   );
// // }

// // export default App;

// import { useState, useEffect } from "react";
// import axios from "axios";

// function App() {
//   const [problem, setProblem] = useState("");
//   const [recommendations, setRecommendations] = useState([]);
//   const [ingredients, setIngredients] = useState([]);
//   const [warnings, setWarnings] = useState("");
//   const [avoid, setAvoid] = useState([]);
//   const [loading, setLoading] = useState(false);
//   const [visibleWarning, setVisibleWarning] = useState(false); // Uyarıyı kontrol eden state

//   useEffect(() => {
//     // Eğer warnings varsa, 3 saniye sonra göster
//     if (warnings) {
//       const timeout = setTimeout(() => {
//         setVisibleWarning(true); // 3 saniye sonra uyarıyı görünür yap
//       }, 3000); // 3000ms = 3 saniye

//       return () => clearTimeout(timeout); // Component unmount olursa timeout'u temizle
//     }
//   }, [warnings]);

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     setLoading(true);
//     setRecommendations([]);
//     setIngredients([]);
//     setAvoid([]);
//     setWarnings("");
//     setVisibleWarning(false); // Yeni bir işlem başladığında uyarıyı gizle

//     try {
//       const response = await axios.post(
//         "http://127.0.0.1:8000/api/recommend/",
//         { problem }
//       );
//       console.log("response.data:", response.data);
//       console.log("recommendations:", response.data.recommendations);
//       console.log("warnings", response.data.warning_message);
//       console.log("ingredients", response.data.ingredients);

//       setRecommendations(response.data.recommendations);
//       setWarnings(response.data.warning_message);
//       setIngredients(response.data.ingredients);
//       setAvoid(response.data.avoid);
//     } catch (error) {
//       console.error("Error fetching recommendations:", error);
//     }

//     setLoading(false);
//   };

//   return (
//     <div className="container">
//       <h1>Skincare Advisor</h1>
//       <form onSubmit={handleSubmit}>
//         <textarea
//           value={problem}
//           onChange={(e) => setProblem(e.target.value)}
//           placeholder="Describe your skin problem..."
//         />
//         <button type="submit" disabled={loading}>
//           {loading ? "Analyzing..." : "Get Advice"}
//         </button>
//       </form>

//       {recommendations.length > 0 && (
//         <div>
//           <h2>Recommendations:</h2>
//           <ul>
//             {recommendations.map((rec, index) => (
//               <li key={index}>{rec}</li>
//             ))}
//           </ul>
//         </div>
//       )}
//       {ingredients.length > 0 && (
//         <div>
//           <h2>Ingredients:</h2>
//           <ul>
//             {ingredients.map((rec, index) => (
//               <li key={index}>{rec}</li>
//             ))}
//           </ul>
//         </div>
//       )}
//       <p>{avoid.join(", ")}</p>

//       {visibleWarning && warnings && (
//         <div
//           style={{
//             whiteSpace: "pre-line", // Satır sonlarını ve boşlukları korur
//             padding: "20px", // Tüm kenarlara 20px padding ekler
//             backgroundColor: "#f8d7da", // Arka plan rengi (isteğe bağlı)
//             border: "1px solid #f5c6cb", // Kenar rengi (isteğe bağlı)
//             borderRadius: "5px", // Kenarları yuvarlatmak (isteğe bağlı)
//           }}
//           dangerouslySetInnerHTML={{
//             __html: warnings,
//           }}
//         />
//       )}
//     </div>
//   );
// }

// export default App;
import React, { useState } from "react";

function App() {
  const [problem, setProblem] = useState("");
  const [advice, setAdvice] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    const response = await fetch("http://localhost:8000/api/get_advice/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ problem }),
    });

    const data = await response.json();
    setLoading(false);

    if (data.advice) {
      setAdvice(data.advice);
    } else {
      setAdvice("Sorry, we couldn't generate advice.");
    }
  };

  return (
    <div className="App">
      <h1>Skincare Advisor</h1>
      <textarea
        value={problem}
        onChange={(e) => setProblem(e.target.value)}
        placeholder="Describe your skin problem..."
      />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Generating Advice..." : "Get Advice"}
      </button>
      {advice && (
        <div>
          <h2>Advice:</h2>
          <p>{advice}</p>
        </div>
      )}
    </div>
  );
}

export default App;
