import React, { useState } from 'react';
import Input from './Input';
import Button from './Button';

const AddTransactionForm = ({ type, onSubmit, onCancel }) => {
  const today = new Date().toISOString().split('T')[0];
  const [formData, setFormData] = useState({
    amount: '',
    description: '',
    source: '',
    date: today,
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    // Create a clean copy of the data to send
    const submissionData = {
      ...formData,
      // Ensure amount is sent as a string to avoid precision issues
      // and matching what your Django logic expects
      amount: parseFloat(formData.amount).toFixed(2) 
    };

    try {
      await onSubmit(submissionData); // Pass the cleaned data
      setFormData({
        amount: '',
        description: '',
        source: '',
        date: today,
      });
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Input
        label="Amount ($)"
        type="number"
        name="amount"
        value={formData.amount}
        onChange={handleChange}
        placeholder="0.00"
        required
        step="0.01"
        min="0.01"
      />

      {type === 'Income' ? (
        <Input
          label="Source"
          type="text"
          name="source"
          value={formData.source}
          onChange={handleChange}
          placeholder="e.g., Salary, Freelance, Gift"
          required
        />
      ) : (
        <Input
          label="Description"
          type="text"
          name="description"
          value={formData.description}
          onChange={handleChange}
          placeholder="e.g., Groceries, Rent, Entertainment"
          required
        />
      )}

      <Input
        label="Date"
        type="date"
        name="date"
        value={formData.date}
        onChange={handleChange}
        required
        max={today}
      />

      <div style={{ display: 'flex', gap: '16px', marginTop: '24px' }}>
        <Button
          type="submit"
          variant="primary"
          size="large"
          fullWidth
          disabled={loading}
        >
          {loading ? 'Adding...' : `Add ${type}`}
        </Button>
        <Button
          type="button"
          variant="secondary"
          size="large"
          onClick={onCancel}
          disabled={loading}
        >
          Cancel
        </Button>
      </div>
    </form>
  );
};

export default AddTransactionForm;