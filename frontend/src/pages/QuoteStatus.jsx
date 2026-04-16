import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';
import { ArrowLeft, MessageCircle, CheckCircle, Circle, Clock } from 'lucide-react';

const QuoteStatus = () => {
  const { quoteNumber } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const [quoteData, setQuoteData] = useState(location.state?.quoteData || null);
  const [loading, setLoading] = useState(!quoteData);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!quoteData) {
      fetchQuoteData();
    }
  }, [quoteNumber]);

  const fetchQuoteData = async () => {
    try {
      const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${BACKEND_URL}/api/leads/track/${quoteNumber}`);
      
      if (!response.ok) {
        setError('Quote not found');
        setLoading(false);
        return;
      }

      const data = await response.json();
      setQuoteData(data);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching quote:', err);
      setError('Failed to load quote status');
      setLoading(false);
    }
  };

  const getStatusIcon = (step) => {
    if (step.completed && !step.current) {
      return <CheckCircle className="timeline-icon completed" />;
    } else if (step.current) {
      return <Circle className="timeline-icon current pulse" />;
    } else {
      return <Circle className="timeline-icon pending" />;
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return null;
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', { 
      day: 'numeric', 
      month: 'short', 
      year: 'numeric' 
    });
  };

  if (loading) {
    return (
      <div className="quote-status-page">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading quote status...</p>
        </div>
      </div>
    );
  }

  if (error || !quoteData) {
    return (
      <div className="quote-status-page">
        <div className="error-container">
          <h2>Quote Not Found</h2>
          <p>{error || 'Unable to load quote status'}</p>
          <Button onClick={() => navigate('/track')}>Try Again</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="quote-status-page">
      <div className="status-header">
        <Button 
          variant="ghost" 
          onClick={() => navigate('/track')}
          className="back-button"
        >
          <ArrowLeft className="mr-2 h-4 w-4" /> Track Another Quote
        </Button>
      </div>

      <div className="status-container">
        {/* Quote Information Card */}
        <Card className="quote-info-card">
          <CardContent className="quote-info-content">
            <div className="quote-header-section">
              <div className="quote-number-display">
                <span className="quote-label">Quote ID</span>
                <h1 className="quote-number">{quoteData.quote_number}</h1>
              </div>
              <div className="quote-status-badge">
                <Clock className="status-icon" />
                <span>In Progress</span>
              </div>
            </div>

            <div className="quote-details-grid">
              <div className="detail-item">
                <span className="detail-label">Customer</span>
                <span className="detail-value">{quoteData.name}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">Service</span>
                <span className="detail-value">{quoteData.service}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">Location</span>
                <span className="detail-value">{quoteData.area}</span>
              </div>
              <div className="detail-item">
                <span className="detail-label">Budget</span>
                <span className="detail-value">{quoteData.budget}</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Timeline Section */}
        <div className="timeline-section">
          <h2 className="timeline-title">Project Timeline</h2>
          <p className="timeline-subtitle">Track your home transformation journey</p>

          <div className="timeline">
            {quoteData.timeline.map((step, index) => (
              <div 
                key={step.status} 
                className={`timeline-item ${step.completed ? 'completed' : ''} ${step.current ? 'current' : ''}`}
              >
                <div className="timeline-marker">
                  {getStatusIcon(step)}
                  {index < quoteData.timeline.length - 1 && (
                    <div className={`timeline-line ${step.completed ? 'completed' : ''}`}></div>
                  )}
                </div>

                <div className="timeline-content">
                  <div className="timeline-header">
                    <h3 className="timeline-step-title">
                      <span className="step-icon">{step.icon}</span>
                      {step.label}
                    </h3>
                    {step.timestamp && (
                      <span className="timeline-date">
                        {formatDate(step.timestamp)}
                      </span>
                    )}
                  </div>
                  <p className="timeline-description">{step.description}</p>
                  {step.note && (
                    <div className="timeline-note">
                      <strong>Note:</strong> {step.note}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* WhatsApp CTA */}
        <Card className="whatsapp-cta-card">
          <CardContent className="whatsapp-cta-content">
            <div className="whatsapp-cta-text">
              <h3>Have questions about your quote?</h3>
              <p>Our team is here to help. Chat with us on WhatsApp.</p>
            </div>
            <Button
              size="lg"
              className="whatsapp-cta-button"
              onClick={() => window.open(`https://wa.me/918551904280?text=Hi,%20I%20have%20a%20question%20about%20my%20quote%20${quoteData.quote_number}`, '_blank')}
            >
              <MessageCircle className="mr-2 h-5 w-5" /> Chat with Us
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default QuoteStatus;
