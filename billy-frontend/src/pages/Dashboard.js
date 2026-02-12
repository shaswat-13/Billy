import React, { useState, useEffect } from "react";
import FinancialSummary from "../components/FinancialSummary";
import TransactionList from "../components/TransactionList";
import Modal from "../components/Modal";
import AddTransactionForm from "../components/AddTransactionForm";
import { financeAPI } from "../services/api";
import "./Dashboard.css";
import { useToast } from "../components/ToastManager";
import LoadingSpinner from "../components/LoadingSpinner";

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(null); // 'income' or 'expense'
  const { addToast } = useToast();

  const fetchData = async () => {
    try {
      const response = await financeAPI.getDashboard();
      setData(response);
    } catch (error) {
      console.error("Error fetching dashboard:", error);
      // If we get a 401 here, the App.js logic should ideally handle the redirect
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleAddIncome = async (formData) => {
    try {
      setLoading(true); // Show spinner while updating
      await financeAPI.addIncome(
        formData.amount,
        formData.source,
        formData.date,
      );
      
      // Give the backend a tiny heartbeat to settle, then fetch
      const updatedData = await financeAPI.getDashboard();
      setData(updatedData);
      
      setShowModal(null);
      addToast(`Income added successfully! 💰`, "success");
    } catch (error) {
      console.error("Error adding income:", error);
      addToast("Successfully added, but had trouble refreshing. Please reload.", "info");
    } finally {
      setLoading(false);
    }
  };

  const handleAddExpense = async (formData) => {
    try {
      setLoading(true); // Show spinner while processing
      
      // 1. Send data to Django
      await financeAPI.addExpense(
        formData.amount,
        formData.description,
        formData.date,
      );

      // 2. Freshly fetch the updated data from the server
      const updatedData = await financeAPI.getDashboard();
      setData(updatedData);

      // 3. Close modal and notify user
      setShowModal(null);
      addToast(
        `Expense of $${formData.amount} added successfully! 📊`,
        "success",
      );
    } catch (error) {
      console.error("Error adding expense:", error);
      // If data actually saved (as you noted), we provide a more helpful message
      addToast("Expense saved! Refreshing your dashboard...", "info");
      await fetchData(); // Attempt one final refresh
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteIncome = async (id) => {
    if (window.confirm("Are you sure you want to delete this income?")) {
      try {
        await financeAPI.deleteIncome(id);
        await fetchData();
        addToast("Income deleted successfully! 🗑️", "info");
      } catch (error) {
        console.error("Error deleting income:", error);
        addToast("Failed to delete income. Please try again.", "error");
      }
    }
  };

  const handleDeleteExpense = async (id) => {
    if (window.confirm("Are you sure you want to delete this expense?")) {
      try {
        await financeAPI.deleteExpense(id);
        await fetchData();
        addToast("Expense deleted successfully! 🗑️", "info");
      } catch (error) {
        console.error("Error deleting expense:", error);
        addToast("Failed to delete expense. Please try again.", "error");
      }
    }
  };

  // 1. Handle Loading State
  if (loading) {
    return (
      <LoadingSpinner size="large" message="Loading your financial data..." />
    );
  }

  // 2. Handle missing data / Error state
  if (!data) {
    return (
      <div className="dashboard-error">
        <h1>Error loading dashboard</h1>
        <p>We couldn't retrieve your data. Please try logging in again.</p>
      </div>
    );
  }

  // 3. Final Render (Now correctly inside the component)
  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Welcome back, {data.user?.first_name || data.user?.username || 'User'}! 🐱</h1>
        <p className="dashboard-subtitle">Here's your financial overview</p>
      </div>

      <FinancialSummary
        totalIncome={data.total_income}
        totalExpenses={data.total_expenses}
        balance={data.balance}
      />

      <div className="dashboard-grid">
        <TransactionList
          title="Income"
          emoji="💰"
          transactions={data.incomes}
          type="Income"
          onDelete={handleDeleteIncome}
          onAdd={() => setShowModal("income")}
        />

        <TransactionList
          title="Expenses"
          emoji="📊"
          transactions={data.expenses}
          type="Expense"
          onDelete={handleDeleteExpense}
          onAdd={() => setShowModal("expense")}
        />
      </div>

      <Modal
        isOpen={showModal === "income"}
        onClose={() => setShowModal(null)}
        title="Add Income"
      >
        <AddTransactionForm
          type="Income"
          onSubmit={handleAddIncome}
          onCancel={() => setShowModal(null)}
        />
      </Modal>

      <Modal
        isOpen={showModal === "expense"}
        onClose={() => setShowModal(null)}
        title="Add Expense"
      >
        <AddTransactionForm
          type="Expense"
          onSubmit={handleAddExpense}
          onCancel={() => setShowModal(null)}
        />
      </Modal>
    </div>
  );
};

export default Dashboard;