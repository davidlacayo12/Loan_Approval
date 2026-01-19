import { useState } from "react";
import { InputRow } from "./components/InputRow";
import { PredictionCard } from "./components/PredictionCard";
import { ArrowPathIcon } from "@heroicons/react/24/solid";

type Payload = {
  city: string;
  income: number;
  credit_score: number;
  loan_amount: number;
  years_employed: number;
};

type Prediction = {
  payload: Payload;
  result: string;
};

function App() {
  const [form, setForm] = useState({
    city: "",
    income: "",
    credit_score: "",
    loan_amount: "",
    years_employed: "",
  });

  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<Prediction[]>([]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    const payload = {
      city: form.city,
      income: Number(form.income),
      credit_score: Number(form.credit_score),
      loan_amount: Number(form.loan_amount),
      years_employed: Number(form.years_employed),
    };

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await res.json();
      const result = data.loan_approved ? "✅ Approved" : "❌ Denied";
      setHistory([{ payload, result }, ...history]);
    } catch (err) {
      console.error(err);
      setHistory([{ payload, result: "⚠️ Error" }, ...history]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-6 text-center text-gray-800">
          Loan Approval Dashboard
        </h1>

        {/* Input Form */}
        <div className="bg-white p-6 rounded shadow-md mb-6">
          <h2 className="text-2xl font-semibold mb-4">Check a Loan</h2>
          <form onSubmit={handleSubmit}>
            <InputRow
              label="City"
              name="city"
              value={form.city}
              onChange={handleChange}
              placeholder="Enter city"
              helper="City of the applicant"
              required
            />
            <InputRow
              label="Income"
              name="income"
              type="number"
              value={form.income}
              onChange={handleChange}
              placeholder="0"
              helper="Income in USD"
              min={0}
              required
            />
            <InputRow
              label="Credit Score"
              name="credit_score"
              type="number"
              value={form.credit_score}
              onChange={handleChange}
              placeholder="300-850"
              helper="FICO score (300-850)"
              min={300}
              max={850}
              required
            />
            <InputRow
              label="Loan Amount"
              name="loan_amount"
              type="number"
              value={form.loan_amount}
              onChange={handleChange}
              placeholder="0"
              helper="Requested amount in USD"
              min={0}
              required
            />
            <InputRow
              label="Years Employed"
              name="years_employed"
              type="number"
              value={form.years_employed}
              onChange={handleChange}
              placeholder="1"
              helper="Number of years employed"
              min={1}
              max={50}
              required
            />

            <button
              type="submit"
              className="mt-4 w-full flex justify-center items-center bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
              disabled={loading}
            >
              {loading && <ArrowPathIcon className="w-5 h-5 animate-spin mr-2" />}
              {loading ? "Checking..." : "Check Loan"}
            </button>
          </form>
        </div>

        {/* Prediction History */}
        <div className="bg-white p-6 rounded shadow-md">
          <h2 className="text-2xl font-semibold mb-4">Recent Predictions</h2>
          {history.length === 0 && (
            <p className="text-gray-500">No predictions yet.</p>
          )}
          <div className="space-y-4">
            {history.map((entry, idx) => (
              <PredictionCard key={idx} payload={entry.payload} result={entry.result} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
