import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { productsAPI, matchesAPI, swipeAPI } from '../services/api';
import { MapPin, Star, Heart, MessageCircle, ShoppingCart, User, Calendar } from 'lucide-react';
import Button from '../components/ui/Button';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';

const ProductDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isLiked, setIsLiked] = useState(false);
  const [showContactForm, setShowContactForm] = useState(false);

  useEffect(() => {
    fetchProduct();
  }, [id]);

  const fetchProduct = async () => {
    try {
      const response = await productsAPI.getById(id);
      setProduct(response.data);
    } catch (error) {
      console.error('Failed to fetch product:', error);
      navigate('/marketplace');
    } finally {
      setLoading(false);
    }
  };

  const handleLike = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    try {
      await swipeAPI.create({
        user_id: user.id,
        action_type: 'right',
        produce_listing_id: parseInt(id)
      });
      setIsLiked(true);
    } catch (error) {
      console.error('Failed to like product:', error);
    }
  };

  const handleContact = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    try {
      await matchesAPI.create({
        buyer_id: user.id,
        produce_listing_id: parseInt(id),
        status: 'pending'
      });
      setShowContactForm(true);
    } catch (error) {
      console.error('Failed to create match:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-green-600"></div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Product not found</h2>
          <Button onClick={() => navigate('/marketplace')}>
            Back to Marketplace
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Product Images */}
          <div>
            <div className="aspect-w-16 aspect-h-12 mb-4">
              <img
                src={product.image || 'https://images.pexels.com/photos/1300972/pexels-photo-1300972.jpeg'}
                alt={product.title}
                className="w-full h-96 object-cover rounded-lg shadow-lg"
              />
            </div>
            
            {/* Additional Images */}
            <div className="grid grid-cols-4 gap-2">
              {[1, 2, 3, 4].map((i) => (
                <img
                  key={i}
                  src={`https://images.pexels.com/photos/${1300972 + i}/pexels-photo-${1300972 + i}.jpeg?auto=compress&cs=tinysrgb&w=200`}
                  alt={`${product.title} ${i}`}
                  className="w-full h-20 object-cover rounded-md cursor-pointer hover:opacity-75 transition-opacity"
                />
              ))}
            </div>
          </div>

          {/* Product Info */}
          <div>
            <div className="mb-6">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{product.title}</h1>
              <div className="flex items-center mb-4">
                <div className="flex items-center">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                  <span className="ml-2 text-gray-600">(4.8) • 24 reviews</span>
                </div>
              </div>
              
              <div className="flex items-center text-gray-600 mb-4">
                <MapPin className="w-5 h-5 mr-2" />
                {product.location}
              </div>
            </div>

            {/* Price and Availability */}
            <Card className="mb-6">
              <CardContent className="p-6">
                <div className="flex justify-between items-center mb-4">
                  <div>
                    <div className="text-3xl font-bold text-green-600">
                      ${product.price_per_unit}
                      <span className="text-lg text-gray-500 font-normal">
                        /{product.unit_of_measurement}
                      </span>
                    </div>
                    <p className="text-gray-600">
                      Available: {product.quantity_available} {product.unit_of_measurement}
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="inline-flex px-3 py-1 text-sm font-semibold rounded-full bg-green-100 text-green-800">
                      In Stock
                    </span>
                  </div>
                </div>

                <div className="flex space-x-3">
                  <Button
                    onClick={handleLike}
                    variant={isLiked ? "primary" : "outline"}
                    className="flex-1"
                  >
                    <Heart className={`w-4 h-4 mr-2 ${isLiked ? 'fill-current' : ''}`} />
                    {isLiked ? 'Liked' : 'Like'}
                  </Button>
                  <Button onClick={handleContact} className="flex-1">
                    <MessageCircle className="w-4 h-4 mr-2" />
                    Contact Farmer
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Description */}
            <Card className="mb-6">
              <CardHeader>
                <CardTitle>Description</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-700 leading-relaxed">
                  {product.description || 'Fresh, high-quality produce grown with care using sustainable farming practices. Our products are harvested at peak ripeness to ensure maximum flavor and nutritional value.'}
                </p>
              </CardContent>
            </Card>

            {/* Farmer Info */}
            <Card>
              <CardHeader>
                <CardTitle>About the Farmer</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex items-center mb-4">
                  <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                    <User className="w-6 h-6 text-green-600" />
                  </div>
                  <div className="ml-4">
                    <h4 className="font-semibold">John Smith Farm</h4>
                    <p className="text-gray-600">Organic farmer since 2010</p>
                  </div>
                </div>
                <div className="flex items-center text-sm text-gray-600 mb-2">
                  <Calendar className="w-4 h-4 mr-2" />
                  Member since 2020
                </div>
                <div className="flex items-center text-sm text-gray-600">
                  <Star className="w-4 h-4 mr-2 text-yellow-400 fill-current" />
                  4.9 rating • 156 reviews
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Contact Form Modal */}
        {showContactForm && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <Card className="max-w-md w-full mx-4">
              <CardHeader>
                <CardTitle>Contact Farmer</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 mb-4">
                  Your interest has been sent to the farmer. They will contact you soon!
                </p>
                <Button
                  onClick={() => setShowContactForm(false)}
                  className="w-full"
                >
                  Close
                </Button>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductDetail;