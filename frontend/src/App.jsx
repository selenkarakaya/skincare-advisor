import { useState } from "react";
import axios from "axios";

function App() {
  const [problem, setProblem] = useState("");
  const [recommendations, setRecommendations] = useState([]);
  const [ingredients, setIngredients] = useState([]);
  const [warnings, setWarnings] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setRecommendations([]); // Eski önerileri temizle
    setWarnings("");

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/recommend/",
        { problem }
      );
      console.log("response.data:", response.data);
      console.log("recommendations:", response.data.recommendations);
      console.log("warnings", response.data.warning_message);
      console.log("ingredients", response.data.ingredients);

      setRecommendations(response.data.recommendations);
      setWarnings(response.data.warning_message);
      setIngredients(response.data.ingredients);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1>Skincare Advisor</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          value={problem}
          onChange={(e) => setProblem(e.target.value)}
          placeholder="Describe your skin problem..."
        />
        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Get Advice"}
        </button>
      </form>

      {recommendations.length > 0 && (
        <div>
          <h2>Recommendations:</h2>
          <ul>
            {recommendations.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
        </div>
      )}
      {ingredients.length > 0 && (
        <div>
          <h2>ingredients:</h2>
          <ul>
            {ingredients.map((rec, index) => (
              <li key={index}>{rec}</li>
            ))}
          </ul>
        </div>
      )}
      <p>{warnings}</p>
      {/* {warnings.length > 0 && (
        <div className="warnings">
          <h2>Warning:</h2>
          <ul>
            {warnings.map((warning, index) => (
              <li key={index} className="warning-message">
                {warning}
              </li>
            ))}
          </ul>
        </div>
      )} */}
    </div>
  );
}

export default App;
