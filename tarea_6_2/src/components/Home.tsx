import EmployeeList from "./EmployeList";
import ProductList from "./ProductList";
import { Button } from "./ui/button";

const Home = ({
  setIsLogin,
  isEmployee,
}: {
  setIsLogin: (value: boolean) => void;
  isEmployee: boolean;
}) => {
  return (
    <div className="w-full h-screen">
      <div className="flex justify-end mb-4 px-16 pt-8">
        <Button onClick={() => setIsLogin(false)}>Cerrar sesión</Button>
      </div>
      <div className="p-5 mx-10 md:mx-24 md:mx-64">
        {isEmployee ? (
          <>
            <h1 className="text-2xl font-bold mb-4">Lista de usuarios</h1>
            <EmployeeList />
          </>
        ) : null}
        <h1 className="text-2xl font-bold mb-4">Lista de productos</h1>
        <ProductList />
      </div>
    </div>
  );
};
export default Home;
