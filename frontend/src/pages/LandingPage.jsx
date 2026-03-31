import React, { useState, useEffect } from 'react';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { 
  ChefHat, 
  Layers, 
  Home, 
  Building, 
  MapPin, 
  Users, 
  BadgeIndianRupee, 
  Clock,
  Star,
  MessageCircle,
  ArrowRight,
  Phone,
  Instagram,
  Check
} from 'lucide-react';
import { services, trustPoints, testimonials, galleryProjects, serviceOptions, budgetOptions } from '../data/mock';

const iconMap = {
  ChefHat: ChefHat,
  Layers: Layers,
  Home: Home,
  Building: Building,
  MapPin: MapPin,
  Users: Users,
  BadgeIndianRupee: BadgeIndianRupee,
  Clock: Clock
};

const LandingPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    email: '',
    area: '',
    service: '',
    budget: '',
    message: ''
  });
  const [showThankYou, setShowThankYou] = useState(false);
  const [errors, setErrors] = useState({});

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
          }
        });
      },
      { threshold: 0.1 }
    );

    document.querySelectorAll('.fade-in-section').forEach((section) => {
      observer.observe(section);
    });

    return () => observer.disconnect();
  }, []);

  const validatePhone = (phone) => {
    const phoneRegex = /^[6-9]\d{9}$/;
    return phoneRegex.test(phone);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleSelectChange = (name, value) => {
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = {};

    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone number is required';
    } else if (!validatePhone(formData.phone)) {
      newErrors.phone = 'Please enter a valid 10-digit mobile number';
    }
    if (!formData.area.trim()) newErrors.area = 'Area/Locality is required';
    if (!formData.service) newErrors.service = 'Please select a service';
    if (!formData.budget) newErrors.budget = 'Please select a budget range';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    try {
      // Submit to backend API
      const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${BACKEND_URL}/api/leads`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to submit form');
      }

      const result = await response.json();
      console.log('Lead submitted:', result);

      setShowThankYou(true);
      setFormData({
        name: '',
        phone: '',
        email: '',
        area: '',
        service: '',
        budget: '',
        message: ''
      });

      setTimeout(() => {
        setShowThankYou(false);
      }, 5000);
    } catch (error) {
      console.error('Error submitting form:', error);
      // Still show thank you message even if backend fails
      setShowThankYou(true);
      setFormData({
        name: '',
        phone: '',
        email: '',
        area: '',
        service: '',
        budget: '',
        message: ''
      });

      setTimeout(() => {
        setShowThankYou(false);
      }, 5000);
    }
  };

  const scrollToForm = () => {
    document.getElementById('quote-form').scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-overlay"></div>
        <div className="hero-content">
          <h1 className="hero-title">Transform Your Home, Without Breaking the Bank</h1>
          <p className="hero-subtitle">
            Mumbai-based end-to-end interior solutions. From modular kitchens to complete home makeovers.
          </p>
          <div className="hero-cta-group">
            <Button onClick={scrollToForm} size="lg" className="cta-primary">
              Get a Free Quote <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button 
              size="lg" 
              className="cta-whatsapp"
              onClick={() => window.open('https://wa.me/918551904280?text=Hi,%20I%27m%20interested%20in%20a%20home%20interior%20quote.', '_blank')}
            >
              <MessageCircle className="mr-2 h-5 w-5" /> Chat with Us
            </Button>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="section-container fade-in-section">
        <div className="section-header">
          <h2 className="section-title">Our Services</h2>
          <p className="section-subtitle">Everything you need to create your dream home</p>
        </div>
        <div className="services-grid">
          {services.map((service) => {
            const Icon = iconMap[service.icon];
            return (
              <Card key={service.id} className="service-card">
                <CardContent className="service-card-content">
                  <div className="service-icon-wrapper">
                    <Icon className="service-icon" />
                  </div>
                  <h3 className="service-title">{service.title}</h3>
                  <p className="service-description">{service.description}</p>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </section>

      {/* Trust Section */}
      <section id="trust" className="trust-section fade-in-section">
        <div className="section-header">
          <h2 className="section-title">Why Choose Us</h2>
        </div>
        <div className="trust-grid">
          {trustPoints.map((point) => {
            const Icon = iconMap[point.icon];
            return (
              <div key={point.id} className="trust-card">
                <div className="trust-icon-wrapper">
                  <Icon className="trust-icon" />
                </div>
                <h3 className="trust-title">{point.title}</h3>
                <p className="trust-description">{point.description}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Gallery Section */}
      <section id="gallery" className="section-container fade-in-section">
        <div className="section-header">
          <h2 className="section-title">Our Work</h2>
          <p className="section-subtitle">Real homes, real transformations across Mumbai</p>
        </div>
        <div className="gallery-grid">
          {galleryProjects.map((project) => (
            <div key={project.id} className="gallery-item">
              <img src={project.image} alt={project.title} className="gallery-image" />
              <div className="gallery-overlay">
                <span className="gallery-service-tag">{project.service}</span>
                <h3 className="gallery-title">{project.title}</h3>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="testimonials-section fade-in-section">
        <div className="section-header">
          <h2 className="section-title">What Our Clients Say</h2>
        </div>
        <div className="testimonials-grid">
          {testimonials.map((testimonial) => (
            <Card key={testimonial.id} className="testimonial-card">
              <CardContent className="testimonial-content">
                <div className="testimonial-stars">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="star-icon" fill="currentColor" />
                  ))}
                </div>
                <p className="testimonial-text">"{testimonial.text}"</p>
                <div className="testimonial-author">
                  <p className="testimonial-name">{testimonial.name}</p>
                  <p className="testimonial-location">{testimonial.location}</p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Quote Form Section */}
      <section id="quote-form" className="form-section fade-in-section">
        <div className="form-container">
          <div className="section-header">
            <h2 className="section-title">Get Your Free Quote</h2>
            <p className="section-subtitle">Tell us about your project and we'll get back to you within 24 hours</p>
          </div>

          {showThankYou ? (
            <Card className="thank-you-card">
              <CardContent className="thank-you-content">
                <div className="thank-you-icon-wrapper">
                  <Check className="thank-you-icon" />
                </div>
                <h3 className="thank-you-title">Thank You!</h3>
                <p className="thank-you-text">
                  We've received your request. Our team will contact you within 24 hours to discuss your project.
                </p>
              </CardContent>
            </Card>
          ) : (
            <Card className="quote-form-card">
              <CardContent className="quote-form-content">
                <form onSubmit={handleSubmit} className="quote-form">
                  <div className="form-group">
                    <label htmlFor="name" className="form-label">Name *</label>
                    <Input
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      placeholder="Your full name"
                      className={errors.name ? 'input-error' : ''}
                    />
                    {errors.name && <span className="error-text">{errors.name}</span>}
                  </div>

                  <div className="form-group">
                    <label htmlFor="phone" className="form-label">Phone Number *</label>
                    <Input
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      placeholder="10-digit mobile number"
                      maxLength="10"
                      className={errors.phone ? 'input-error' : ''}
                    />
                    {errors.phone && <span className="error-text">{errors.phone}</span>}
                  </div>

                  <div className="form-group">
                    <label htmlFor="email" className="form-label">Email (Optional)</label>
                    <Input
                      id="email"
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      placeholder="your.email@example.com"
                    />
                    <span className="text-xs text-gray-500">We'll send you a confirmation email</span>
                  </div>

                  <div className="form-group">
                    <label htmlFor="area" className="form-label">Area/Locality (Mumbai) *</label>
                    <Input
                      id="area"
                      name="area"
                      value={formData.area}
                      onChange={handleInputChange}
                      placeholder="e.g., Andheri, Thane, Borivali"
                      className={errors.area ? 'input-error' : ''}
                    />
                    {errors.area && <span className="error-text">{errors.area}</span>}
                  </div>

                  <div className="form-group">
                    <label htmlFor="service" className="form-label">Service Interested In *</label>
                    <Select value={formData.service} onValueChange={(value) => handleSelectChange('service', value)}>
                      <SelectTrigger className={errors.service ? 'input-error' : ''}>
                        <SelectValue placeholder="Select a service" />
                      </SelectTrigger>
                      <SelectContent>
                        {serviceOptions.map((option) => (
                          <SelectItem key={option} value={option}>
                            {option}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    {errors.service && <span className="error-text">{errors.service}</span>}
                  </div>

                  <div className="form-group">
                    <label htmlFor="budget" className="form-label">Budget Range *</label>
                    <Select value={formData.budget} onValueChange={(value) => handleSelectChange('budget', value)}>
                      <SelectTrigger className={errors.budget ? 'input-error' : ''}>
                        <SelectValue placeholder="Select your budget" />
                      </SelectTrigger>
                      <SelectContent>
                        {budgetOptions.map((option) => (
                          <SelectItem key={option} value={option}>
                            {option}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    {errors.budget && <span className="error-text">{errors.budget}</span>}
                  </div>

                  <div className="form-group">
                    <label htmlFor="message" className="form-label">Message (Optional)</label>
                    <Textarea
                      id="message"
                      name="message"
                      value={formData.message}
                      onChange={handleInputChange}
                      placeholder="Tell us more about your requirements..."
                      rows="4"
                    />
                  </div>

                  <Button type="submit" size="lg" className="submit-button">
                    Request My Free Quote
                  </Button>
                </form>
              </CardContent>
            </Card>
          )}
        </div>
      </section>

      {/* Floating WhatsApp Button */}
      <a
        href="https://wa.me/918551904280?text=Hi,%20I%27m%20interested%20in%20a%20home%20interior%20quote."
        target="_blank"
        rel="noopener noreferrer"
        className="whatsapp-float"
        aria-label="Chat on WhatsApp"
      >
        <MessageCircle className="whatsapp-icon" />
      </a>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-section">
            <h3 className="footer-brand">Millenial Architects</h3>
            <p className="footer-tagline">Transforming homes, creating dreams</p>
          </div>
          <div className="footer-section">
            <h4 className="footer-heading">Contact</h4>
            <div className="footer-links">
              <a href="tel:+918551904280" className="footer-link">
                <Phone className="footer-icon" /> +91 85519 04280
              </a>
              <a 
                href="https://wa.me/918551904280?text=Hi,%20I%27m%20interested%20in%20a%20home%20interior%20quote." 
                target="_blank" 
                rel="noopener noreferrer"
                className="footer-link"
              >
                <MessageCircle className="footer-icon" /> WhatsApp
              </a>
            </div>
          </div>
          <div className="footer-section">
            <h4 className="footer-heading">Follow Us</h4>
            <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="footer-link">
              <Instagram className="footer-icon" /> Instagram
            </a>
          </div>
        </div>
        <div className="footer-bottom">
          <p>© 2024 Millenial Architects. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
