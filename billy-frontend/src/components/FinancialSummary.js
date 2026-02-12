import React from 'react';
import Card from './Card';
import './FinancialSummary.css';

const FinancialSummary = ({ totalIncome, totalExpenses, balance }) => {
  return (
    <Card emoji="💰" title="Financial Summary" className="financial-summary">
      <div className="summary-grid">
        <div className="summary-item income">
          <span className="summary-label">Total Income</span>
          <span className="summary-value">${parseFloat(totalIncome).toFixed(2)}</span>
        </div>

        <div className="summary-item expense">
          <span className="summary-label">Total Expenses</span>
          <span className="summary-value">${parseFloat(totalExpenses).toFixed(2)}</span>
        </div>

        <div className="summary-item balance">
          <span className="summary-label">Balance</span>
          <span className={`summary-value ${parseFloat(balance) >= 0 ? 'positive' : 'negative'}`}>
            ${parseFloat(balance).toFixed(2)}
          </span>
        </div>
      </div>
    </Card>
  );
};

export default FinancialSummary;