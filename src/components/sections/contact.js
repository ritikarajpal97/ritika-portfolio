import React, { useEffect, useRef } from 'react';
import styled from 'styled-components';
import { srConfig, email } from '@config';
import sr from '@utils/sr';
import { usePrefersReducedMotion } from '@hooks';
import IconLinkedin from '@components/icons/linkedin';

const StyledContactSection = styled.section`
  max-width: 600px;
  margin: 0 auto 100px;
  text-align: center;

  @media (max-width: 768px) {
    margin: 0 auto 50px;
  }

  .overline {
    display: block;
    margin-bottom: 20px;
    color: var(--green);
    font-family: var(--font-mono);
    font-size: var(--fz-md);
    font-weight: 400;

    &:before {
      bottom: 0;
      font-size: var(--fz-sm);
    }

    &:after {
      display: none;
    }
  }

  .title {
    font-size: clamp(40px, 5vw, 60px);
  }

  .contact-buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 50px;
  }

  .contact-btn {
    ${({ theme }) => theme.mixins.bigButton};
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 16px;

    svg {
      width: 22px;
      height: 22px;
      fill: none;
    }
  }
`;

const Contact = () => {
  const revealContainer = useRef(null);
  const prefersReducedMotion = usePrefersReducedMotion();

  useEffect(() => {
    if (prefersReducedMotion) {
      return;
    }

    sr.reveal(revealContainer.current, srConfig());
  }, []);

  return (
    <StyledContactSection id="contact" ref={revealContainer}>
      <h2 className="numbered-heading overline">What’s Next?</h2>

      <h2 className="title">Get In Touch</h2>

      <p>
        Whether it’s product, AI, new opportunities, or just a good conversation, I’m always down. Say hello!
      </p>

      <div className="contact-buttons">
        <a className="contact-btn" href={`mailto:${email}`} aria-label="Send email">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <polyline points="2,4 12,13 22,4"></polyline>
            <path d="M2 4h20v16a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V4z" fill="none"></path>
          </svg>
        </a>
        <a className="contact-btn" href="https://www.linkedin.com/in/ritika-rajpal" target="_blank" rel="noreferrer" aria-label="LinkedIn profile">
          <IconLinkedin />
        </a>
      </div>
    </StyledContactSection>
  );
};

export default Contact;
