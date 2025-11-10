# Example Makefiles for Testing

This directory contains example Makefiles for testing the autotools-language-server.

## Files

### Makefile (Linux Kernel Top-level Makefile)

This is the top-level Makefile from the Linux kernel (v6.18-rc5). It's a complex, real-world example that demonstrates the language server's capabilities on production code.

**Test Results:**

The language server successfully parses the file but reports several issues:

1. **Parser Limitations**: The tree-sitter parser has difficulty with advanced Make syntax, particularly:

   - Conditional variable names: `stackp-flags-$(CONFIG_STACKPROTECTOR) := ...`
   - Dynamic include directives: `include-$(CONFIG_DEBUG_INFO) += ...`
   - Complex function syntax with operators

2. **Expected Warnings**: Many warnings about repeated targets, which is valid in Makefiles where targets can have multiple rules with different prerequisites.

3. **Missing Dependencies**: One error about missing `include/config/auto.conf.cmd`, which is expected since we don't have the full kernel build tree.

**Statistics:**

- Size: ~70KB
- \~2,100 lines
- Includes advanced Make features: pattern rules, functions, conditionals, includes

### test.mk (Simple Example)

A simple, clean Makefile that demonstrates basic features:

- Variable assignments
- Pattern rules
- PHONY targets
- Automatic variables

**Test Results:** ✓ No errors or warnings

## Running the Tests

To check a Makefile for errors:

```bash
autotools-language-server --check example/Makefile
autotools-language-server --check example/test.mk
```

## Observations

The Linux kernel Makefile is an excellent stress test because it:

- Uses nearly every Make feature
- Has complex conditional logic
- Includes dynamic variable and target names
- Demonstrates real-world complexity

The errors found primarily reflect limitations in the tree-sitter-make parser rather than actual Makefile syntax errors. The kernel Makefile builds successfully with GNU Make 4.0+.
