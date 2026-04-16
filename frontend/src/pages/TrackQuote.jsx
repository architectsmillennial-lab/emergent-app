import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent } from '../components/ui/card';
import { Search, ArrowLeft } from 'lucide-react';

const TrackQuote = () => {
  const [quoteNumber, setQuoteNumber] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleTrack = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!quoteNumber.trim()) {
      setError('Please enter your Quote ID');
      return;
    }

    setLoading(true);

    try {
      const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
      const response = await fetch(`${BACKEND_URL}/api/leads/track/${quoteNumber.trim()}`);
      
      if (!response.ok) {
        if (response.status === 404) {
          setError('Quote ID not found. Please check and try again.');
        } else {
          setError('Unable to track quote. Please try again.');
        }
        setLoading(false);
        return;
      }

      const data = await response.json();
      navigate(`/track/${quoteNumber.trim()}`, { state: { quoteData: data } });
    } catch (err) {
      console.error('Error tracking quote:', err);
      setError('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="track-quote-page">
      <div className="track-header">
        <Button 
          variant="ghost" 
          onClick={() => navigate('/')}
          className="back-button"
        >
          <ArrowLeft className="mr-2 h-4 w-4" /> Back to Home
        </Button>
      </div>

      <div className="track-container">
        <div className="track-content">
          <h1 className="track-title">Track Your Quote</h1>
          <p className="track-subtitle">
            Enter your Quote ID to check the status of your interior design project
          </p>

          <Card className="track-card">
            <CardContent className="track-card-content">
              <form onSubmit={handleTrack} className="track-form">
                <div className="form-group">
                  <label htmlFor="quoteNumber" className="form-label">
                    Quote ID
                  </label>
                  <div className="input-with-icon">
                    <Input
                      id="quoteNumber"
                      value={quoteNumber}
                      onChange={(e) => setQuoteNumber(e.target.value.toUpperCase())}
                      placeholder="MA-2026-00142"
                      className="quote-input"
                      disabled={loading}
                    />
                    <Search className="input-icon" />
                  </div>
                  <span className="input-hint">
                    Format: MA-YYYY-XXXXX (e.g., MA-2026-00142)
                  </span>
                  {error && <span className="error-text">{error}</span>}
                </div>

                <Button 
                  type="submit" 
                  size="lg" 
                  className="track-submit-button"
                  disabled={loading}
                >
                  {loading ? 'Tracking...' : 'Track Quote'}
                </Button>
              </form>

              <div className="track-help">
                <p className="help-text">
                  <strong>Where to find your Quote ID?</strong>
                </p>
                <ul className="help-list">
                  <li>Check the confirmation screen after submitting your quote</li>
                  <li>Look for it in the confirmation email we sent you</li>
                  <li>It's in the format MA-2026-XXXXX</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          <div className="track-features">
            <div className="feature-item">
              <div className="feature-icon">📍</div>
              <div className="feature-text">
                <h3>Real-time Updates</h3>
                <p>See exactly where your project stands</p>
              </div>
            </div>
            <div className="feature-item">
              <div className="feature-icon">🏠</div>
              <div className="feature-text">
                <h3>From Quote to Completion</h3>
                <p>Track every stage of your home transformation</p>
              </div>
            </div>
            <div className="feature-item">
              <div className="feature-icon">💬</div>
              <div className="feature-text">
                <h3>Stay Connected</h3>
                <p>Reach out anytime via WhatsApp</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrackQuote;
