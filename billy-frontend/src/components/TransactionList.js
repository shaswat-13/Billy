import React from 'react';
import Card from './Card';
import Button from './Button';
import './TransactionList.css';

const TransactionList = ({ title, emoji, transactions, type, onDelete, onAdd }) => {
  const isEmpty = transactions.length === 0;

  return (
    <Card emoji={emoji} title={title} className="transaction-list">
      <div className="transaction-header">
        <Button variant="primary" size="small" onClick={onAdd}>
          ➕ Add {type}
        </Button>
      </div>

      {isEmpty ? (
        <div className="empty-state">
          <p>No {type.toLowerCase()} records yet.</p>
          <p>Click the button above to add your first one!</p>
        </div>
      ) : (
        <div className="transactions">
          {transactions.map((transaction) => (
            <div key={transaction.id} className="transaction-item paper">
              <div className="transaction-info">
                <span className="transaction-name">
                  {transaction.source || transaction.description}
                </span>
                <span className="transaction-date">{transaction.date}</span>
              </div>
              <div className="transaction-actions">
                <span className="transaction-amount">
                  ${parseFloat(transaction.amount).toFixed(2)}
                </span>
                <Button
                  variant="danger"
                  size="small"
                  onClick={() => onDelete(transaction.id)}
                >
                  🗑️
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </Card>
  );
};

export default TransactionList;