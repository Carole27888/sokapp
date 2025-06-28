import { Link } from 'react-router-dom';
import { ArrowRight, Users, ShoppingBag, TrendingUp, Star } from 'lucide-react';
import Button from '../components/ui/Button';

const Home = () => {
  const features = [
    {
      icon: <Users className="w-8 h-8 text-green-600" />,
      title: 'Connect Farmers & Buyers',
      description: 'Direct connection between farmers and buyers, eliminating middlemen and ensuring fair prices.'
    },
    {
      icon: <ShoppingBag className="w-8 h-8 text-green-600" />,
      title: 'Fresh Produce Marketplace',
      description: 'Browse and purchase fresh, locally-sourced produce directly from verified farmers.'
    },
    {
      icon: <TrendingUp className="w-8 h-8 text-green-600" />,
      title: 'Market Analytics',
      description: 'Access real-time market data and pricing trends to make informed decisions.'
    }
  ];

  const testimonials = [
    {
      name: 'John Smith',
      role: 'Organic Farmer',
      content: 'AgriConnect has transformed how I sell my produce. Direct access to buyers means better prices and less waste.',
      rating: 5
    },
    {
      name: 'Sarah Johnson',
      role: 'Restaurant Owner',
      content: 'Finding fresh, local ingredients has never been easier. The quality is exceptional and delivery is reliable.',
      rating: 5
    },
    {
      name: 'Mike Chen',
      role: 'Grocery Store Manager',
      content: 'The platform streamlines our sourcing process and helps us support local farmers while offering competitive prices.',
      rating: 5
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-green-600 to-green-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              Connecting Farmers with the World
            </h1>
            <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
              Join the agricultural revolution. Buy fresh produce directly from farmers 
              or sell your harvest to a global marketplace.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/marketplace">
                <Button size="lg" variant="secondary" className="w-full sm:w-auto">
                  Browse Marketplace
                  <ArrowRight className="ml-2 w-5 h-5" />
                </Button>
              </Link>
              <Link to="/register">
                <Button size="lg" className="w-full sm:w-auto bg-white text-green-600 hover:bg-gray-100">
                  Join as Farmer
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose AgriConnect?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Our platform brings together technology and agriculture to create 
              a sustainable and profitable ecosystem for everyone.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="bg-white p-8 rounded-lg shadow-md text-center">
                <div className="flex justify-center mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-4">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-green-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold mb-2">10,000+</div>
              <div className="text-green-200">Active Farmers</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">50,000+</div>
              <div className="text-green-200">Products Listed</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">1M+</div>
              <div className="text-green-200">Successful Transactions</div>
            </div>
            <div>
              <div className="text-4xl font-bold mb-2">500+</div>
              <div className="text-green-200">Cities Served</div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              What Our Users Say
            </h2>
            <p className="text-xl text-gray-600">
              Hear from farmers and buyers who have transformed their business with AgriConnect.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="bg-white p-6 rounded-lg shadow-md">
                <div className="flex mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-gray-600 mb-4">"{testimonial.content}"</p>
                <div>
                  <div className="font-semibold">{testimonial.name}</div>
                  <div className="text-sm text-gray-500">{testimonial.role}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Ready to Get Started?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Join thousands of farmers and buyers who are already benefiting from our platform.
          </p>
          <Link to="/register">
            <Button size="lg" className="bg-green-600 hover:bg-green-700">
              Create Your Account Today
              <ArrowRight className="ml-2 w-5 h-5" />
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;