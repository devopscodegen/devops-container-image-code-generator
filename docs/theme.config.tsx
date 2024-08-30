import React from 'react';
import { useRouter } from 'next/router'
import type { DocsThemeConfig } from 'nextra-theme-docs'
import { useConfig } from 'nextra-theme-docs'

const config: DocsThemeConfig = {
  logo: (
    <span>
      <img
        src="/devops-container-image-code-generator/logo.svg"
        width="48"
        style={{ display: 'inline-block' }}
      />
      <span style={{ paddingLeft: '12px' }}>DevOps container image code generator</span>
    </span>
  ),
  useNextSeoProps() {
    const { asPath } = useRouter()
    if (asPath !== '/') {
      return {
        titleTemplate: '%s – DevOps container image code generator'
      }
    }
  },
  project: {
    link: 'https://github.com/devopscodegen/devops-container-image-code-generator',
  },
  docsRepositoryBase:
    'https://github.com/devopscodegen/devops-container-image-code-generator/tree/main/docs',
  footer: {
    text: (
      <span>
        DevOps container image code generator | Built by <a href="/">Sagar Velankar</a>
      </span>
    ),
  },
  head: function useHead() {
    const { title } = useConfig()
    const socialCard = 'https://devopscodegen.github.io/devops-container-image-code-generator/og.svg'

    return (
      <>
        <meta name="msapplication-TileColor" content="#fff" />
        <meta name="theme-color" content="#fff" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta httpEquiv="Content-Language" content="en" />
        <meta
          name="description"
          content="DevOps container image code generator"
        />
        <meta
          name="og:description"
          content="DevOps container image code generator"
        />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:image" content={socialCard} />
        <meta name="twitter:site:domain" content="devopscodegen.github.io" />
        <meta name="twitter:url" content="https://devopscodegen.github.io" />
        <meta
          name="og:title"
          content={title ? title + ' – DevOps container image code generator' : 'DevOps container image code generator'}
        />
        <meta name="og:image" content={socialCard} />
        <meta name="apple-mobile-web-app-title" content="DevOps container image code generator" />
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
        <link rel="icon" href="/favicon.png" type="image/png" />
        <link
          rel="icon"
          href="/favicon-dark.svg"
          type="image/svg+xml"
          media="(prefers-color-scheme: dark)"
        />
        <link
          rel="icon"
          href="/favicon-dark.png"
          type="image/png"
          media="(prefers-color-scheme: dark)"
        />
      </>
    )
  },
  editLink: {
    text: 'Edit this page on GitHub →'
  },
  feedback: {
    content: 'Question? Give us feedback →',
    labels: 'feedback'
  },
  sidebar: {
    titleComponent({ title, type }) {
      if (type === 'separator') {
        return <span className="cursor-default">{title}</span>
      }
      return <>{title}</>
    },
    defaultMenuCollapseLevel: 1,
    toggleButton: true
  },
  toc: {
    backToTop: true
  }
};

export default config;
