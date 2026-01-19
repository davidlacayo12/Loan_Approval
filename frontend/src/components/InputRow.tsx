import React from "react";

type Props = {
  label: string;
  name: string;
  type?: "text" | "number";
  value: string | number;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  helper?: string;
  min?: number;
  max?: number;
  required?: boolean;
};

export const InputRow: React.FC<Props> = ({
  label,
  name,
  type = "text",
  value,
  onChange,
  placeholder,
  helper,
  min,
  max,
  required = false,
}) => {
  return (
    <div className="flex flex-col sm:flex-row sm:items-center mb-4">
      <label className="sm:w-40 font-medium text-gray-700">{label}:</label>
      <div className="flex-1">
        <input
          type={type}
          name={name}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-400"
          min={min}
          max={max}
          required={required}
        />
        {helper && <p className="text-gray-400 text-sm mt-1">{helper}</p>}
      </div>
    </div>
  );
};
