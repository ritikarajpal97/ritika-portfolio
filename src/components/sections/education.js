import React, { useEffect, useRef } from 'react';
import { useStaticQuery, graphql } from 'gatsby';
import styled from 'styled-components';
import { srConfig } from '@config';
import sr from '@utils/sr';
import { usePrefersReducedMotion } from '@hooks';

const StyledEducationSection = styled.section`
  max-width: 700px;

  .education-grid {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-top: 30px;
    padding: 0;
    list-style: none;
  }
`;

const StyledEducationCard = styled.li`
  ${({ theme }) => theme.mixins.boxShadow};
  padding: 25px 30px;
  border-radius: var(--border-radius);
  background-color: var(--light-navy);
  transition: var(--transition);

  @media (prefers-reduced-motion: no-preference) {
    &:hover,
    &:focus-within {
      transform: translateY(-4px);
    }
  }

  h3 {
    margin: 0 0 6px;
    font-size: var(--fz-xl);
    font-weight: 500;
    line-height: 1.3;
    color: var(--lightest-slate);
  }

  .school {
    color: var(--green);
    font-size: var(--fz-lg);

    a {
      ${({ theme }) => theme.mixins.inlineLink};
    }
  }

  .meta {
    margin: 6px 0 18px;
    color: var(--light-slate);
    font-family: var(--font-mono);
    font-size: var(--fz-xs);
  }

  ul {
    ${({ theme }) => theme.mixins.fancyList};
    margin: 0;
  }
`;

const Education = () => {
  const data = useStaticQuery(graphql`
    query {
      education: allMarkdownRemark(
        filter: { fileAbsolutePath: { regex: "/content/education/" } }
        sort: { fields: [frontmatter___date], order: DESC }
      ) {
        edges {
          node {
            frontmatter {
              degree
              school
              location
              range
              url
            }
            html
          }
        }
      }
    }
  `);

  const revealContainer = useRef(null);
  const prefersReducedMotion = usePrefersReducedMotion();

  useEffect(() => {
    if (prefersReducedMotion) {
      return;
    }
    sr.reveal(revealContainer.current, srConfig());
  }, []);

  return (
    <StyledEducationSection id="education" ref={revealContainer}>
      <h2 className="numbered-heading">Education</h2>

      <ul className="education-grid">
        {data.education.edges.map(({ node }, i) => {
          const { degree, school, location, range, url } = node.frontmatter;
          return (
            <StyledEducationCard key={i}>
              <h3>{degree}</h3>
              <div className="school">
                {url ? (
                  <a href={url} target="_blank" rel="noreferrer">
                    {school}
                  </a>
                ) : (
                  school
                )}
              </div>
              <p className="meta">
                {location} &middot; {range}
              </p>
              <div dangerouslySetInnerHTML={{ __html: node.html }} />
            </StyledEducationCard>
          );
        })}
      </ul>
    </StyledEducationSection>
  );
};

export default Education;
