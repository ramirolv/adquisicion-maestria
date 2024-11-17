import InputForm from "./components/InputForm";
import { Toaster } from "@/components/ui/toaster";
import "./App.css";
import { useState } from "react";
import Home from "./components/Home";

function App() {
  const [isLogin, setIsLogin] = useState(false);
  const [isEmployee, setIsEmployee] = useState(false);
  return (
    <>
      {!isLogin ? (
        <div className="flex w-full justify-center items-center h-screen bg-slate-300">
          <InputForm setIsLogin={setIsLogin} setIsEmployee={setIsEmployee} />
        </div>
      ) : (
        <Home setIsLogin={setIsLogin} isEmployee={isEmployee} />
      )}
      <Toaster />
    </>
  );
}

export default App;
