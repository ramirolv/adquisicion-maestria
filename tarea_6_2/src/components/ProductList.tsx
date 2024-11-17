import { useEffect, useState } from "react";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";

interface Product {
  id: number
  title: string
  price: number
  description: string
  images: string[]
  category: {
    name: string;
  };
}

export default function ProductList() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("https://api.escuelajs.co/api/v1/products")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch products");
        }
        return response.json();
      })
      .then((data) => {
        setProducts(data);
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
    <div className="max-h-[800px] overflow-y-auto">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
        {products.map((product) => (
          <Card key={product.id} className="w-full">
            <CardHeader>
              <img
                src={`https://picsum.photos/id/${product.id}/200/300`}
                alt={product.title}
                className="w-full h-48 object-cover rounded-t-lg"
              />
            </CardHeader>
            <CardContent>
              <CardTitle className="mb-2 line-clamp-1">{product.title}</CardTitle>
              <p className="text-sm text-muted-foreground mb-2 line-clamp-2">{product.description}</p>
              <Badge variant="secondary" className="mb-2">
                {product.category.name}
              </Badge>
            </CardContent>
            <CardFooter className="flex justify-between items-center">
              <span className="text-lg font-bold">Q {product.price.toFixed(2)}</span>
              <button className="bg-primary text-primary-foreground hover:bg-primary/90 px-4 py-2 rounded">
                Agregar al carrito
              </button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  )
}
