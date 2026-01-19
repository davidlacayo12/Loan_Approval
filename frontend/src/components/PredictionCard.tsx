import React from "react";

type Payload = {
  city: string;
  income: number;
  credit_score: number;
  loan_amount: number;
  years_employed: number;
};

type Props = {
  payload: Payload;
  result: string;
};

export const PredictionCard: React.FC<Props> = ({ payload, result }) => {
  const colorClass =
    result.includes("Approved")
      ? "border-green-500 bg-green-50"
      : result.includes("Denied")
      ? "border-red-500 bg-red-50"
      : "border-yellow-500 bg-yellow-50";

  return (
    <div className={`p-4 rounded border-l-4 ${colorClass}`}>
      <div className="flex justify-between items-center mb-1">
        <span className="font-semibold">{result}</span>
        <span className="text-gray-500 text-sm">{new Date().toLocaleTimeString()}</span>
      </div>
      <div className="text-gray-700 text-sm space-y-1">
        <div>City: {payload.city}</div>
        <div>Income: ${payload.income.toLocaleString()}</div>
        <div>Credit Score: {payload.credit_score}</div>
        <div>Loan Amount: ${payload.loan_amount.toLocaleString()}</div>
        <div>Years Employed: {payload.years_employed}</div>
      </div>
    </div>
  );
};
