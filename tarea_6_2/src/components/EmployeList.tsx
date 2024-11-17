import { useEffect, useState } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";

interface Employee {
  id: number
  name: string
  email: string 
  password: string
  role: string
  avatar: string
  creationAt: string
  updatedAt: string
};

export default function EmployeeList() {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("https://api.escuelajs.co/api/v1/users")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch products");
        }
        return response.json();
      })
      .then((data) => {
        setEmployees(data);
        setLoading(false);
      })
      .catch(() => {
        setError("Error fetching products. Please try again later.");
        setLoading(false);
      })
  }, [])

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
        {[...Array(6)].map((_, index) => (
          <Card key={index} className="w-full">
            <CardHeader>
              <Skeleton className="h-48 w-full" />
            </CardHeader>
            <CardContent>
              <Skeleton className="h-4 w-2/3 mb-2" />
              <Skeleton className="h-4 w-1/2" />
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (error) {
    return <div className="text-center text-red-500 p-6">{error}</div>
  }

  return (
    <div className="max-w-full overflow-x-auto">
      <div className="flex gap-6 p-3">
        {employees.map((employee) => (
          <Card key={employee.id} className="w-60 flex-shrink-0">
            <CardHeader>
              <img
                src={employee.avatar}
                alt={employee.name}
                className="w-full h-36 object-cover rounded-t-lg"
              />
            </CardHeader>
            <CardContent>
              <CardTitle className="line-clamp-1">{employee.name}</CardTitle>
              <p className="text-sm text-muted-foreground mb-2 line-clamp-2">{employee.email}</p>
              <Badge variant="secondary" className="">
                {employee.role}
              </Badge>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}