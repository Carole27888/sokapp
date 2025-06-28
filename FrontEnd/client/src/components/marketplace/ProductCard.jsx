import { Link } from 'react-router-dom';
import { MapPin, Star, Heart } from 'lucide-react';
import { Card, CardContent } from '../ui/Card';
import Button from '../ui/Button';

const ProductCard = ({ product, onLike, isLiked = false }) => {
  return (
    <Card className="hover:shadow-lg transition-shadow">
      <div className="relative">
        <img
          src={product.image || 'https://images.pexels.com/photos/1300972/pexels-photo-1300972.jpeg'}
          alt={product.title}
          className="w-full h-48 object-cover rounded-t-lg"
        />
        <button
          onClick={() => onLike && onLike(product.id)}
          className={`absolute top-2 right-2 p-2 rounded-full ${
            isLiked ? 'bg-red-500 text-white' : 'bg-white text-gray-600'
          } hover:scale-110 transition-transform`}
        >
          <Heart className={`w-4 h-4 ${isLiked ? 'fill-current' : ''}`} />
        </button>
      </div>
      
      <CardContent className="p-4">
        <h3 className="font-semibold text-lg mb-2 line-clamp-1">{product.title}</h3>
        <p className="text-gray-600 text-sm mb-3 line-clamp-2">
          {product.description || 'Fresh, high-quality produce from local farmers.'}
        </p>
        
        <div className="flex items-center justify-between mb-3">
          <div className="text-2xl font-bold text-green-600">
            ${product.price_per_unit}
            <span className="text-sm text-gray-500 font-normal">
              /{product.unit_of_measurement}
            </span>
          </div>
          <div className="flex items-center">
            <Star className="w-4 h-4 text-yellow-400 fill-current" />
            <span className="text-sm text-gray-600 ml-1">4.8</span>
          </div>
        </div>
        
        <div className="flex items-center text-sm text-gray-500 mb-3">
          <MapPin className="w-4 h-4 mr-1" />
          {product.location}
        </div>
        
        <div className="text-sm text-gray-600 mb-4">
          Available: {product.quantity_available} {product.unit_of_measurement}
        </div>
        
        <Link to={`/product/${product.id}`}>
          <Button className="w-full">
            View Details
          </Button>
        </Link>
      </CardContent>
    </Card>
  );
};

export default ProductCard;